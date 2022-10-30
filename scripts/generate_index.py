import json
import pickle
import re
import string

import fire
import pandas as pd
from loguru import logger
from sentence_transformers import SentenceTransformer


def process(paper: dict):
    year_pattern = r"(19|20[0-9]{2})"

    paper = json.loads(paper)
    if paper["journal-ref"]:
        years = [int(year) for year in re.findall(year_pattern, paper["journal-ref"])]
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


def papers(year_cutoff: int, ml_category: str, data_path: str):
    with open(data_path, "r") as f:
        for paper in f:
            paper = process(paper)
            if paper["year"]:
                if paper["year"] >= year_cutoff and ml_category in paper["categories"]:
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


def run(year_cutoff = 2012, ml_category = "cs.LG", data_path = "arxiv-metadata-oai-snapshot.json"):
    logger.info("Reading papers...")
    df = pd.DataFrame(papers(year_cutoff, ml_category, data_path))

    length = len(df)
    mean = df.abstract.apply(lambda a: len(a.split())).mean()

    logger.info(f"Length: {length}")
    logger.info(f"Mean: {mean}")

    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    logger.info("Creating embeddings from the title and abstract...")
    emb = model.encode(
        df.apply(
            lambda r: clean_description(r["title"] + " " + r["abstract"]), axis=1
        ).tolist()
    )

    logger.info("Adding embeddings...")
    df = df.reset_index().drop("index", axis=1)
    df["vector"] = emb.tolist()

    logger.info("Exporting to pickle file...")
    with open("arxiv_embeddings_10000.pkl", "wb") as f:
        data = pickle.dumps(df)
        f.write(data)


if __name__ == "__main__":
    fire.Fire(run)
