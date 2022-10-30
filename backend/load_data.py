import fire
import asyncio
import datetime
import os
import pickle
import typing as t
from typing import Optional

import numpy as np
import redis.asyncio as redis
from redis.commands.search.field import TagField
from redis_om import get_redis_connection
from thm.config.settings import get_settings
from thm.models import Paper
from thm.search_index import SearchIndex

from loguru import logger

CONCURRENCY_LEVEL = 5
SEPARATOR = "|"


def read_paper_df() -> t.List:
    with open(f"{config.data_location}/arxiv_embeddings_10000.pkl", "rb") as f:
        df = pickle.load(f)
    return df


async def gather_with_concurrency(n, separator, *papers):
    semaphore = asyncio.Semaphore(n)

    async def load_paper(paper):
        async with semaphore:
            vector = paper.pop("vector")
            paper["paper_id"] = paper.pop("id")
            # TODO - we need to be able to use other separators
            paper["categories"] = paper["categories"].replace(",", separator)
            p = Paper(**paper)
            # save model TODO -- combine these two objects eventually
            await p.save()

            # save vector data
            # key = "paper_vector:" + str(p.paper_id)
            # await redis_conn.hset(
            #     key,
            #     mapping={
            #         "paper_pk": p.pk,
            #         "paper_id": p.paper_id,
            #         "categories": p.categories,
            #         "year": p.year,
            #         "vector": np.array(vector, dtype=np.float32).tobytes(),
            #     },
            # )

    # gather with concurrency
    await asyncio.gather(*[load_paper(p) for p in papers])


async def load_all_data():
    redis_conn = redis.from_url(config.get_redis_url())
    search_index = SearchIndex()

    if await redis_conn.dbsize() > 300:
        logger.info("Papers already loaded")
    else:
        logger.info("Loading papers into Vecsim App")
        papers = read_paper_df()
        papers = papers.to_dict("records")
        await gather_with_concurrency(CONCURRENCY_LEVEL, SEPARATOR, *papers)
        logger.info("Papers loaded!")

        logger.info("Creating vector search index")
        categories_field = TagField("categories", separator="|")
        year_field = TagField("year", separator="|")

        # create a search index
        if config.index_type == "HNSW":
            await search_index.create_hnsw(
                categories_field,
                year_field,
                redis_conn=redis_conn,
                number_of_vectors=len(papers),
                prefix="paper_vector:",
                distance_metric="IP",
            )
        else:
            await search_index.create_flat(
                categories_field,
                year_field,
                redis_conn=redis_conn,
                number_of_vectors=len(papers),
                prefix="paper_vector:",
                distance_metric="IP",
            )
        logger.info("Search index created")


if __name__ == "__main__":

    # TODO CLI arguments --concurrency_level, --separator
    config = get_settings()

    Paper.Meta.database = get_redis_connection(
        url=config.get_redis_url(), decode_responses=True
    )
    Paper.Meta.global_key_prefix = "THM"
    Paper.Meta.model_key_prefix = "Paper"

    # https://github.com/tqdm/tqdm

    # https://github.com/rsalmei/alive-progress
