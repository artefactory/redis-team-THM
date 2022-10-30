import json
import pickle
import re
import string

import fire
import pandas as pd
from loguru import logger
from sentence_transformers import SentenceTransformer

DATA_PATH = "arxiv-metadata-oai-snapshot.json"
YEAR_CUTOFF = 2012
YEAR_PATTERN = r"(19|20[0-9]{2})"
ML_CATEGORY = "cs.LG"


def process(paper: dict):
    paper = json.loads(paper)
    if paper["journal-ref"]:
        years = [int(year) for year in re.findall(YEAR_PATTERN, paper["journal-ref"])]
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


def papers():
    with open(DATA_PATH, "r") as f:
        for paper in f:
            paper = process(paper)
            if paper["year"]:
                if paper["year"] >= YEAR_CUTOFF and ML_CATEGORY in paper["categories"]:
                    yield paper


def clean_description(description: str):
    if not description:
        return ""
    # remove unicode characters
    description = description.encode("ascii", "ignore").decode()

    # remove punctuation
    description = re.sub("[%s]" % re.escape(string.punctuation), " ", description)

    # clean up the spacing
    description = re.sub("\s{2,}", " ", description)

    # remove urls
    # description = re.sub("https*\S+", " ", description)

    # remove newlines
    description = description.replace("\n", " ")

    # remove all numbers
    # description = re.sub('\w*\d+\w*', '', description)

    # split on capitalized words
    description = " ".join(re.split("(?=[A-Z])", description))

    # clean up the spacing again
    description = re.sub("\s{2,}", " ", description)

    # make all words lowercase
    description = description.lower()

    return description


def run():

    logger
    df = pd.DataFrame(papers())
    len(df)

    # Avg length of the abstracts
    df.abstract.apply(lambda a: len(a.split())).mean()

    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    # Create embeddings from the title and abstract
    emb = model.encode(
        df.apply(
            lambda r: clean_description(r["title"] + " " + r["abstract"]), axis=1
        ).tolist()
    )

    # Add embeddings to df
    df = df.reset_index().drop("index", axis=1)
    df["vector"] = emb.tolist()

    logger.info("Exporting to pickle file...")
    with open("arxiv_embeddings_10000.pkl", "wb") as f:
        data = pickle.dumps(df)
        f.write(data)


if __name__ == "__main__":
    fire.Fire(run)
