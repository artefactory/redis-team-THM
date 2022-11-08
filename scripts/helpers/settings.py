from pydantic import BaseSettings

from helpers.models import Format


class Settings(BaseSettings):
    format: Format = Format.BibTeX
    max_results: int = 3
    question_answering_priority_papers: int = 25
    question_answering_model: str = "distilbert-base-cased-distilled-squad"
    question_answering_tokenizer: str = "distilbert-base-cased-distilled-squad"
    classifier_model_location: str = "../backend/model_outputs_20221103181333"
    classifier_tokenizer: str = "prajjwal1/bert-tiny"
    classifier_confidence_threshold: float = 0.1
    year_pattern: str = "(19|20[0-9]{2})"
