import asyncio
import pickle
import struct
from typing import List

import fire
import redis.asyncio as redis
from loguru import logger
from redis.asyncio import Redis
from redis.commands.search.field import TagField
from redis_om import get_redis_connection
from thm.config.settings import get_settings
from thm.models import Paper
from thm.search_index import SearchIndex

CONCURRENCY_LEVEL = 2
SEPARATOR = "|"
VECTOR_SIZE = 768


# TODO can be done faster using pyarrow
def read_paper_df(config) -> List:
    with open(f"{config.embeddings_path}", "rb") as f:
        df = pickle.load(f)
    return df


async def gather_with_concurrency(redis_conn, n, separator, *papers):
    semaphore = asyncio.Semaphore(n)

    async def load_paper(paper):
        async with semaphore:
            await redis_conn.hset(
                f"THM:Paper:{paper['id']}",
                mapping={
                    "paper_id": paper["id"],
                    "title": paper["title"],
                    "authors": paper["authors"],
                    "abstract": paper["abstract"],
                    "categories": paper["categories"].replace(",", separator),
                    "year": paper["year"],
                    "vector": struct.pack("%sf" % VECTOR_SIZE, *paper["vector"]),
                },
            )

    await asyncio.gather(*[load_paper(p) for p in papers])


async def load_all_data(
    config, redis_conn: Redis, concurrency_level: int, separator: str
):
    search_index = SearchIndex()

    if await redis_conn.dbsize() > 300:
        logger.info("Papers already loaded")
    else:
        logger.info("Loading papers...")
        papers = read_paper_df(config)
        papers = papers.to_dict("records")

        logger.info("Writing to Redis...")
        await gather_with_concurrency(redis_conn, concurrency_level, separator, *papers)
        logger.info("Papers loaded!")

        logger.info("Creating vector search index")
        categories_field = TagField("categories", separator=SEPARATOR)
        year_field = TagField("year", separator=SEPARATOR)

        if config.index_type == "HNSW":
            await search_index.create_hnsw(
                categories_field,
                year_field,
                redis_conn=redis_conn,
                number_of_vectors=len(papers),
                prefix="THM:Paper:",
                distance_metric="IP",
            )
        else:
            await search_index.create_flat(
                categories_field,
                year_field,
                redis_conn=redis_conn,
                number_of_vectors=len(papers),
                prefix="THM:Paper:",
                distance_metric="IP",
            )
        logger.info("Search index created")


def run(
    concurrency_level: int = 2,
    separator: str = "|",
    reset_db: bool = False,
):
    """Load the Embedding Index to Redis."""

    config = get_settings()
    logger.info(f"TODO {reset_db}")

    Paper.Meta.database = get_redis_connection(
        url=config.get_redis_url(), decode_responses=True
    )
    Paper.Meta.global_key_prefix = "THM"
    Paper.Meta.model_key_prefix = "Paper"

    redis_conn = redis.from_url(config.get_redis_url())

    asyncio.run(load_all_data(config, redis_conn, concurrency_level, separator))


if __name__ == "__main__":
    fire.Fire(run)

    # https://github.com/tqdm/tqdm
    # https://github.com/rsalmei/alive-progress
