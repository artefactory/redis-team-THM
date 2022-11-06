import asyncio
import pickle
import struct
from typing import List

import fire
import redis.asyncio as redis
import tqdm
from loguru import logger
from redis.asyncio import Redis
from redis.commands.search.field import TagField
from redis_om import get_redis_connection
from thm.config.settings import get_settings
from thm.models import Paper
from thm.search_index import SearchIndex


def read_paper_df(embeddings_path) -> List:
    with open(embeddings_path, "rb") as f:
        df = pickle.load(f)
    return df


async def gather_with_concurrency(redis_conn, n, separator, vector_size, *papers):
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
                    "predicted_categories": paper["predicted_categories"],
                    "year": paper["year"],
                    # "vector": np.array(vector, dtype=np.float32).tobytes(),
                    "vector": struct.pack("%sf" % vector_size, *paper["vector"]),
                },
            )

    flist = [load_paper(p) for p in papers]

    # https://stackoverflow.com/questions/61041214
    [await f for f in tqdm.tqdm(asyncio.as_completed(flist), total=len(flist))]


async def load_all_data(
    config,
    redis_conn: Redis,
    concurrency_level: int,
    separator: str,
    embeddings_path: str,
    vector_size: int,
):
    search_index = SearchIndex()

    logger.info("Loading papers...")
    papers = read_paper_df(embeddings_path)
    papers = papers.to_dict("records")

    logger.info("Writing to Redis...")
    await gather_with_concurrency(
        redis_conn, concurrency_level, separator, vector_size, *papers
    )
    logger.info("Papers loaded!")

    logger.info("Creating vector search index")
    categories_field = TagField("categories", separator=separator)
    year_field = TagField("year", separator=separator)

    if config.index_type == "HNSW":
        await search_index.create_hnsw(
            categories_field,
            year_field,
            redis_conn=redis_conn,
            number_of_vectors=len(papers),
            prefix="THM:Paper:",
            distance_metric="IP",
            vector_size=vector_size,
        )
    else:
        await search_index.create_flat(
            categories_field,
            year_field,
            redis_conn=redis_conn,
            number_of_vectors=len(papers),
            prefix="THM:Paper:",
            distance_metric="IP",
            vector_size=vector_size,
        )
    logger.info("Search index created")


def run(
    concurrency_level: int = 2,
    separator: str = "|",
    reset_db: bool = False,
    embeddings_path: str = "",
    vector_size: int = 768,
):
    """Load the Embedding Index to Redis."""

    config = get_settings()

    if reset_db:
        logger.info(f"TODO {reset_db}")

    Paper.Meta.database = get_redis_connection(
        url=config.get_redis_url(), decode_responses=True
    )
    Paper.Meta.global_key_prefix = "THM"
    Paper.Meta.model_key_prefix = "Paper"

    redis_conn = redis.from_url(config.get_redis_url())

    asyncio.run(
        load_all_data(
            config,
            redis_conn,
            concurrency_level,
            separator,
            embeddings_path,
            vector_size,
        )
    )


if __name__ == "__main__":
    fire.Fire(run)
