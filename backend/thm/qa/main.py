import sys

sys.path.append("backend/")

import os
import pandas as pd
import thm.qa.config as cfg
from arxiv_dataset import data_load
from thm.qa.paper_priority import PriorityPapersManager
from thm.config.settings import get_settings
from transformers import pipeline

DATA_LOCATION = os.environ.get("DATA_LOCATION", '/home/jovyan/arxiv/arxiv-metadata-oai-snapshot.json')
DATA_LOCATION = '/home/jovyan/arxiv/arxiv-metadata-oai-snapshot.json'
YEAR_CUTOFF = 2012
ML_CATEGORY = "cs.LG"

def validate_question(question: str) -> str:
    # TODO: implement validation steps of question
    return question

def papers(): # TODO: load directly from redis
    with open(DATA_LOCATION, 'r') as f:
        for paper in f:
            paper = data_load.parse_paper(paper)
            if paper['year']:
                if paper['year'] >= YEAR_CUTOFF and ML_CATEGORY in paper['categories']:
                    yield paper

def get_prioritized_articles(question: str) -> PriorityPapersManager:
    # TODO: implement search of similar articles
    papers_df = pd.DataFrame(papers())
    contexts = papers_df.apply(
        lambda r: data_load.clean_description(r['title'] + ' ' + r['abstract']), axis=1
    ).tolist()
    contexts = contexts[:100]
    ids = papers_df["id"].iloc[:100]
    
    return PriorityPapersManager(
        paper_contexts=contexts,
        paper_ids = ids,
    )
    
def build_answer(answer):
    raise NotImplementedError

def main(question: str, top_k:int =1):
    validated_question = validate_question(question)
    priority_articles = get_prioritized_articles(validated_question)
    
    # instantiate tokenizer and model
    model = pipeline(task="question-answering", model=cfg.MODEL_NAME, tokenizer=cfg.TOKENIZER_NAME)
    model_outputs = model(
        {
            "question": validated_question,
            "context": priority_articles.merged_context
        },
        top_k=top_k
    )
    
    return model_outputs
    
    # answer = build_answer(model_output)

if __name__ == "__main__":
    main(question="What is Machine Learning?")