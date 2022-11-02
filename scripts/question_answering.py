from typing import Dict, List, Tuple

from transformers import pipeline

from helpers.models import Paper
from helpers.paper_manager import PriorityPapersManager
from helpers.search_engine import SearchEngine
from helpers.settings import Settings

settings = Settings()

def get_prioritized_articles(user_prompt: str) -> PriorityPapersManager:
    engine = SearchEngine("https://docsearch.redisventures.com/api/v1/paper")
    search_papers, _ = engine.search(user_prompt, max_results=settings.question_answering_priority_papers)
    
    # parse list of papers
    papers = []
    papers_text = []
    for paper in search_papers:
        paper = engine.paper(paper.paper_id)
        papers.append(paper)
        
        if paper.abstract and paper.title:
            paper_text = paper.title + " " + paper.abstract
        elif paper.title:
            paper_text = paper.title
        elif paper.abstract:
            paper_text = paper.abstract
        
        papers_text.append(paper_text)
        
    return PriorityPapersManager(papers_text, papers)

def _validate_prompt(user_prompt: str):
    # TODO: implement checks
    return user_prompt

def _build_answer(qa_output: List[Dict], priority_papers: PriorityPapersManager) -> List[Tuple[str, float, Paper]]:
    # builds the object that is exposed to the front
    answer = []
    
    for output in qa_output:
        start_answer = output["start"]
        end_answer = output["end"]
        text_answer = output["answer"]
        confidence_score = output["score"]
        paper = priority_papers.find_paper(target_start=start_answer, target_end=end_answer)
        
        answer.append((text_answer, confidence_score, paper))
    
    return answer

def get_answer_to_prompt(question: str, top_k:int =1):
    validated_question = _validate_prompt(question)
    priority_papers = get_prioritized_articles(validated_question)
    
    # instantiate model
    model = pipeline(
        task="question-answering",
        model=settings.question_answering_model,
        tokenizer=settings.question_answering_tokenizer
    )
    # get predictions
    model_outputs = model(
        {
            "question": validated_question,
            "context": priority_papers.merged_context
        },
        top_k=top_k
    )
    if top_k == 1:
        model_outputs = [model_outputs]
    
    return _build_answer(model_outputs, priority_papers)
