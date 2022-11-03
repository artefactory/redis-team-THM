from helpers.models import Format
from pydantic import BaseSettings


class Settings(BaseSettings):
    format: Format = Format.BibTeX
    max_results: int = 3
    question_answering_priority_papers: int = 25
    question_answering_model: str = "distilbert-base-cased-distilled-squad"
    question_answering_tokenizer: str = "distilbert-base-cased-distilled-squad"
