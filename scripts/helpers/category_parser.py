import json
import re
from typing import Dict, List, Tuple, Union

with open("helpers/categories.json", "r") as categories:
    taxonomy = json.load(categories)


def parse_categories_from_redis(categories: str, sep: str = "|") -> List[str]:
    categories_list = categories.split(sep)
    categories_labels = [taxonomy[category] for category in categories_list]

    return categories_labels

def parse_predicted_categories_from_redis(categories: str) -> List[Tuple[str, float]]:
    categories_list = categories.split("|")
    confidences = list(map(lambda x: float(re.findall(r'\(([^)]+)', x)[0]), categories_list)) # extract numbers between parenthesis and convert to float
    categories = list(map(lambda x: x.split("(")[0], categories_list))
    categories_labels = [taxonomy[category] for category in categories]

    return list(zip(categories_labels, confidences))


def parse_classifier_prediction(
    prediction_dicts: Union[Dict, List[Dict]],
    categories_list: List[str],
    confidence_threshold: float,
) -> str:
    if not isinstance(prediction_dicts, list):  # case of single prediction
        prediction_dicts = [prediction_dicts]

    prediction_strings = []
    for prediction in prediction_dicts:
        if prediction["score"] >= confidence_threshold:
            prediction_label = int(prediction["label"][6:])  # remove 'LABEL_'
            prediction_category = categories_list[prediction_label]

            prediction_strings.append(
                f"{prediction_category}({prediction['score']:0.4f})"
            )

    return "|".join(prediction_strings)
