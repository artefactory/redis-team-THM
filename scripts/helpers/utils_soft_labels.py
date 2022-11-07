import json
import re
import string
from typing import Dict, Tuple

import datasets
import numpy as np
import pandas as pd
import torch
from helpers.settings import Settings
from transformers import AutoTokenizer, Trainer

config = Settings()


def _get_category_names(args: np.array, ooe_df: pd.DataFrame):
    """From the predictions and the ooe_df, get the category names"""
    # get category names from args
    return ooe_df.columns[args[0].astype(int).tolist()]


def integrate_soft_labels_back_in_df(
    df_with_paper_data: pd.DataFrame, preds: np.array, ooe_df: pd.DataFrame
) -> pd.DataFrame:
    """Integrate the soft labels back in the dataframe with papers

    Args:
        df_with_paper_data (pd.DataFrame): input dataframe with papers
        preds (np.array): predictions from the model
        ooe_df (pd.DataFrame): dataframe with one-hot encoded categories

    Returns:
        : pd.DataFrame: dataframe with papers and soft labels
    """
    best_args_score_vec = np.apply_along_axis(_get_best_args_and_score, 1, preds)
    categories_vec = np.apply_along_axis(
        _get_category_names, 1, best_args_score_vec, ooe_df
    )
    best_score = best_args_score_vec[:, 1]
    soft_tags = {
        "category": categories_vec.tolist(),
        "score": np.around(best_score, 2).tolist(),
    }
    df_with_paper_data["category_predicted"] = soft_tags["category"]
    df_with_paper_data["category_predicted"] = df_with_paper_data[
        "category_predicted"
    ].str.join(",")
    df_with_paper_data["category_score"] = soft_tags["score"]
    return df_with_paper_data


def compute_predictions(df_dataset: datasets.Dataset, trainer: Trainer) -> np.array:
    """Compute the predictions for the dataset and apply softmax to obtain values between 0 and 1

    Args:
        df_dataset (datasets.Dataset): dataset to compute the predictions for
        trainer (Trainer): trainer object

    Returns:
        np.array: predictions
    """
    preds = trainer.predict(df_dataset)
    preds = preds.predictions
    preds = torch.nn.functional.softmax(torch.tensor(preds))
    return preds


def apply_tokenenizer(
    df_dataset: datasets.Dataset, tokenizer: AutoTokenizer
) -> datasets.Dataset:
    """Apply the tokenizer to the dataset convert the labels to torch.float

    Args:
        df_dataset (datasets.Dataset): dataset to apply the tokenizer to
        tokenizer (AutoTokenizer): tokenizer to use
    Returns:
        datasets.Dataset: tokenized dataset
    """

    def _tokenize_and_encode(examples):
        return tokenizer(examples["text"], truncation=True)

    cols = df_dataset.column_names
    cols.remove("labels")
    df_dataset = df_dataset.map(_tokenize_and_encode, batched=True, remove_columns=cols)

    df_dataset.set_format("torch")
    df_dataset = df_dataset.map(
        lambda x: {"float_labels": x["labels"].to(torch.float)},
        remove_columns=["labels", "token_type_ids"],
    ).rename_column("float_labels", "labels")
    return df_dataset


def prepare_labels(df: pd.DataFrame) -> Tuple[pd.DataFrame, np.array, int]:
    """Parse the labels and save the names in ooe_df

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    ooe_df = df["categories"].str.get_dummies(sep=",")
    num_classes = ooe_df.shape[1]
    category_cols = ooe_df.columns.tolist()

    def parse_labels(row):
        return [row[c] for c in category_cols]

    # parse the labels
    df["labels"] = ooe_df.apply(parse_labels, axis=1)
    df = df[["text", "labels"]]
    return df, ooe_df, num_classes


def clean_description(description: str) -> str:
    """Clean the description"""
    if not description:
        return ""
    # remove unicode characters
    description = description.encode("ascii", "ignore").decode()

    # remove punctuation
    description = re.sub("[%s]" % re.escape(string.punctuation), " ", description)

    # clean up the spacing
    description = re.sub("\s{2,}", " ", description)

    # remove newlines
    description = description.replace("\n", " ")

    # split on capitalized words
    description = " ".join(re.split("(?=[A-Z])", description))

    # clean up the spacing again
    description = re.sub("\s{2,}", " ", description)

    # make all words lowercase
    description = description.lower()

    return description


# Generator functions that iterate through the file and process/load papers


def process(paper: dict) -> Dict:
    """Process the paper"""
    paper = json.loads(paper)
    if paper["journal-ref"]:
        # Attempt to parse the date using Regex: this could be improved
        years = [
            int(year) for year in re.findall(config.year_pattern, paper["journal-ref"])
        ]
        years = [year for year in years if (year <= 2022 and year >= 1991)]
        year = min(years) if years else None
    else:
        year = None
    return {
        "id": paper["id"],
        "title": paper["title"],
        "year": year,
        "authors": paper["authors"],
        "categories": ",".join(paper["categories"].split(" ")),
        "abstract": paper["abstract"],
    }


def papers(data_location: str):
    """Generator function that iterates through the file and yields papers"""
    with open(data_location, "r") as f:
        for paper in f:
            paper = process(paper)
            # Yield only papers that have a year I could process
            if paper["year"]:
                yield paper


def _get_best_args_and_score(row: np.array) -> Tuple[np.array, np.array]:
    """Get the best arguments and score from the prediction row"""
    # get 3 best predictions
    best_args = np.argpartition(row, -3)[-3:]
    best_score = row[best_args]
    return best_args, best_score
