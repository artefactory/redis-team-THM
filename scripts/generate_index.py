import pickle
from typing import Optional

import fire
import pandas as pd
from helpers.processors import clean_description, process
from loguru import logger
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

tqdm.pandas()


def get_papers(data_path: str, year_month: Optional[int] = None):
    with open(data_path, "r") as f:
        for paper in f:
            paper = process(paper)
            if paper["year"]:
                if year_month is None:
                    yield paper
                elif int(paper["update_date"][:7].replace("-", "")) == year_month:
                    yield paper


def _featurize(model, title, abstract):
    sentence = clean_description(f"{title} {abstract}")
    return model.encode(sentence).tolist()


def run(
    year_month,
    input_path="arxiv-metadata-oai-snapshot.json",
    output_path="arxiv_embeddings_10000.pkl",
    model_name="sentence-transformers/all-mpnet-base-v2",
):
    """Generate Embeddings and Create a File Index."""

    logger.info(f"Reading papers for {year_month}...")
    df = pd.DataFrame(get_papers(input_path, year_month))

    # https://www.sbert.net/docs/usage/semantic_textual_similarity.html
    model = SentenceTransformer(model_name)

    logger.info("Creating embeddings from title and abstract...")
    logger.info(model_name)

    df["vector"] = df.progress_apply(
        lambda x: _featurize(model, x["title"], x["abstract"]), axis=1
    )
    df = df.reset_index().drop("index", axis=1)

    df = df.reset_index().drop("index", axis=1)

    logger.info("Exporting to pickle file...")
    with open(output_path, "wb") as f:
        data = pickle.dumps(df)
        f.write(data)


if __name__ == "__main__":
    fire.Fire(run)
