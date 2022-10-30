from typing import Tuple, Union

import thm.qa.config as cfg
import torch
from thm.qa.paper_priority import PriorityPapersManager
from torch.nn.functional import softmax
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers.tokenization_utils_base import BatchEncoding


def tokenize_text(question: str, priority_articles: PriorityPapersManager, tokenizer: AutoTokenizer) -> BatchEncoding:
    tokenized_text = tokenizer(
        question,
        priority_articles.merged_context,
        add_special_tokens=True, # add BERT special tokens [CLS] and [SEP]
        return_tensors="pt", # use pytorch as backend
        truncation="only_second", #source: https://huggingface.co/course/chapter7/7?fw=tf#preparing-the-data:~:text=truncation%3D%22only_second%22%20to%20truncate%20the%20context%20(which%20is%20in%20the%20second%20position)%20when%20the%20question%20with%20its%20context%20is%20too%20long
        padding=True,
        return_overflowing_tokens=True,
        stride=cfg.TOKENIZER_STRIDE
    )
    
    del tokenized_text["overflow_to_sample_mapping"] # managed by PriorityPapersManager
    
    return tokenized_text
    

def extract_answer(tokenized_text: BatchEncoding, model: AutoModelForQuestionAnswering, tokenizer: AutoTokenizer) -> Union[Tuple[str, float], None]:
    answer_scores = model(**tokenized_text)
    # extract scores for the starting tokens and end tokens
    answer_start_scores = answer_scores.start_logits
    answer_end_scores = answer_scores.end_logits
    # compute confidence scores
    confidence_start = torch.max(softmax(answer_start_scores.flatten()))
    confidence_end = torch.max(softmax(answer_end_scores.flatten()))
    confidence_score = float(confidence_start * confidence_end)
    
    # extract start and end 
    answer_start = torch.argmax(answer_start_scores)  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
    
    if answer_start == answer_end:
        return None # empty prediction
    
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(
            tokenized_text["input_ids"].flatten()[answer_start:answer_end] # extract answer
        )
    )
    
    return (answer, confidence_score)
