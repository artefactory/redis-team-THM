import pickle
from functools import partial

import pandas as pd
from helpers.category_parser import parse_classifier_prediction
from helpers.settings import Settings
from loguru import logger
from helpers.utils_soft_labels import clean_description  # need to add to pythonpath
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TextClassificationPipeline,
)

settings = Settings()


def get_paper_classification_predictions(
    raw_text_column: pd.Series, top_k: int
) -> pd.Series:
    logger.info("Loading artifacts")
    model = AutoModelForSequenceClassification.from_pretrained(
        f"{settings.classifier_model_location}/model_outputs"
    )
    with open(f"{settings.classifier_model_location}/categories.pkl", "rb") as cat_file:
        categories = pickle.load(cat_file)

    logger.info("Cleaning data...")
    clean_text_column = raw_text_column.apply(clean_description)

    logger.info("Loading model and tokenizer")
    tokenizer = AutoTokenizer.from_pretrained(
        settings.classifier_tokenizer,
        problem_type="multi_label_classification",
        model_max_length=512,
    )

    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer)

    logger.info("Getting predictions...")
    predictions = clean_text_column.apply(
        partial(pipeline, top_k=top_k, truncation=True)
    )
    parsed_predictions = predictions.apply(
        partial(
            parse_classifier_prediction,
            categories_list=categories,
            confidence_threshold=settings.classifier_confidence_threshold,
        )
    )
    logger.info("Done with predictions")

    return parsed_predictions
