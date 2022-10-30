import os
from argparse import ArgumentParser
from typing import Tuple, Union

import backend.qa.config as cfg
import pandas as pd
import torch
from backend.arxiv_dataset import data_load
from backend.qa.paper_priority import PriorityPapersManager
from torch.nn.functional import softmax
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers.tokenization_utils_base import BatchEncoding


def validate_question(question: str) -> str:
    # TODO: implement validation steps of question
    return question

def get_prioritized_articles(question: str) -> PriorityPapersManager:
    # TODO: implement search of similar articles
    DATA_LOCATION = os.environ.get("DATA_LOCATION", '/home/jovyan/arxiv/arxiv-metadata-oai-snapshot.json')
    DATA_LOCATION = '/home/jovyan/arxiv/arxiv-metadata-oai-snapshot.json'
    YEAR_CUTOFF = 2012
    ML_CATEGORY = "cs.LG"
    def papers():
        with open(DATA_LOCATION, 'r') as f:
            for paper in f:
                paper = data_load.parse_paper(paper)
                if paper['year']:
                    if paper['year'] >= YEAR_CUTOFF and ML_CATEGORY in paper['categories']:
                        yield paper
    
    papers_df = pd.DataFrame(papers())
    contexts = papers_df.apply(
        lambda r: data_load.clean_description(r['title'] + ' ' + r['abstract']), axis=1
    ).tolist()
    contexts = contexts[:100]
    ids = papers_df.papers_df.iloc[:100]
    
    return PriorityPapersManager(
        paper_contexts=contexts,
        paper_ids = ids,
    )
    

def tokenize_text(question: str, prioritized_articles: PriorityPapersManager, tokenizer: AutoTokenizer) -> BatchEncoding:
    tokenized_text = tokenizer(
        question,
        prioritized_articles.merged_context,
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
    
def build_answer(answer):
    raise NotImplementedError

def main(question: str):
    validated_question = validate_question(question)
    priority_articles = get_prioritized_articles(validated_question)
    
    # instantiate tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(cfg.TOKENIZER_NAME)
    model = AutoModelForQuestionAnswering.from_pretrained(cfg.MODEL_NAME)
    
    model_input = tokenize_text(
        question=validated_question, 
        priority_articles=priority_articles,
        tokenizer=tokenizer
    )
    model_output = extract_answer(
        tokenized_text=model_input,
        model=model
    )
    
    # answer = build_answer(model_output)

if __name__ == "__main__":
    parser = ArgumentParser(
        description="TODO", # TODO: write description
        
    ) 
    parser.add_argument("--question", "-q", type=str, 
                        required=True, help="The question the user has defined")
    args = parser.parse_args()
    main(**args)
