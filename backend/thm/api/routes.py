import asyncio
from typing import Dict

import redis.asyncio as redis
from fastapi import APIRouter

from thm.config.settings import get_settings
from thm.embeddings import Embeddings
from thm.models import Paper
from thm.schema.search import SimilarityRequest, UserTextSimilarityRequest
from thm.search_index import SearchIndex

from loguru import logger

config = get_settings()

paper_router = r = APIRouter()

redis_client = redis.from_url(config.get_redis_url())
embeddings = Embeddings(config.model_name)
search_index = SearchIndex()


async def process_paper(p) -> Dict:
    logger.info(p.paper_id)

    paper = await Paper.get(p.paper_id)
    paper = paper.dict()
    score = 1 - float(p.vector_score)
    paper["similarity_score"] = score
    return paper


async def papers_from_docs(total, docs) -> list:
    return {
        "total": total,
        "papers": [await process_paper(p) for p in docs],
    }


@r.post("/vectorsearch/text", response_model=Dict)
async def find_papers_by_paper_id(request: SimilarityRequest) -> Dict:
    # Create query
    query = search_index.vector_query(
        request.categories,
        request.years,
        request.search_type,
        request.number_of_results,
    )
    count_query = search_index.count_query(
        years=request.years, categories=request.categories
    )

    # find the vector of the Paper listed in the request
    paper_vector_key = "THM:Paper:" + str(request.paper_id)
    vector = await redis_client.hget(paper_vector_key, "vector")

    # obtain results of the queries
    total, results = await asyncio.gather(
        redis_client.ft(config.index_name).search(count_query),
        redis_client.ft(config.index_name).search(
            query, query_params={"vec_param": vector}
        ),
    )

    # Get Paper records of those results
    return await papers_from_docs(total.total, results.docs)


@r.post("/vectorsearch/text/user", response_model=Dict)
async def find_papers_by_user_text(
    request: UserTextSimilarityRequest,
) -> Dict:
    query = search_index.vector_query(
        request.categories,
        request.years,
        request.search_type,
        request.number_of_results,
    )
    count_query = search_index.count_query(
        years=request.years, categories=request.categories
    )

    total, results = await asyncio.gather(
        redis_client.ft(config.index_name).search(count_query),
        redis_client.ft(config.index_name).search(
            query,
            query_params={"vec_param": embeddings.make(request.user_text).tobytes()},
        ),
    )

    logger.info(total.total)
    logger.info(results.docs)

    return await papers_from_docs(total.total, results.docs)
