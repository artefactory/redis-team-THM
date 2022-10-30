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
        "update_date": paper["update_date"],
        "authors": paper["authors"],
        "categories": ",".join(paper["categories"].split(" ")),
        "abstract": paper["abstract"],
    }


def papers(data_path: str, filters: dict):
    with open(data_path, "r") as f:
        for paper in f:
            paper = process(paper)
            if paper["year"]:
                if filters is None:
                    yield paper
                elif int(paper["update_date"][:7].replace("-","")) == filters["year_month"]:
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


def run(
    year_month,
    input_path="arxiv-metadata-oai-snapshot.json",
    output_path="arxiv_embeddings_10000.pkl",
    model_name="sentence-transformers/all-mpnet-base-v2",
):
    """Generate Embeddings and Create a File Index."""

    filters = {"year_month": year_month}
    logger.info(f"Reading papers for... {filters}")
    df = pd.DataFrame(papers(input_path, filters))

    length = len(df)
    logger.info(length)
    mean = df.abstract.apply(lambda a: len(a.split())).mean()

    logger.info(f"NB of Papers: {length}")
    logger.info(f"Mean Word Count: {mean}")

    # See https://huggingface.co/spaces/mteb/leaderboard
    model = SentenceTransformer(model_name)

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
    with open(output_path, "wb") as f:
        data = pickle.dumps(df)
        f.write(data)


if __name__ == "__main__":
    fire.Fire(run)
