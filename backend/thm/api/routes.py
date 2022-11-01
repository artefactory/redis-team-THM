import asyncio
from typing import Dict

import redis.asyncio as redis
from fastapi import APIRouter

from thm.config.settings import get_settings
from thm.embeddings import Embeddings
from thm.models import Paper
from thm.schema import SimilarityRequest, UserTextSimilarityRequest
from thm.search_index import SearchIndex

config = get_settings()

paper_router = r = APIRouter()
redis_client = redis.from_url(config.get_redis_url)
embeddings = Embeddings()
search_index = SearchIndex()


async def process_paper(p) -> Dict:
    paper = await Paper.get(p.paper_id)
    paper = paper.dict()
    score = 1 - float(p.vector_score)
    paper["similarity_score"] = score
    return paper


async def papers_from_results(total, results) -> list:
    # extract papers from VSS results
    return {
        "total": total,
        "papers": [await process_paper(p) for p in results.docs],
    }

# TODO Read this
# https://redis.readthedocs.io/en/stable/examples/search_vector_similarity_examples.html#Adding-Vector-Fields


@r.get("/", response_model=Dict)
async def get_papers(
    limit: int = 20, skip: int = 0, years: str = "", categories: str = ""
):
    papers = []
    expressions = []
    years = [year for year in years.split(",") if year]
    categories = [cat for cat in categories.split(",") if cat]

    if years and categories:
        expressions.append((Paper.year << years) & (Paper.categories << categories))
    elif years and not categories:
        expressions.append(Paper.year << years)
    elif categories and not years:
        expressions.append(Paper.categories << categories)

    # Run query
    papers = (
        await Paper.find(*expressions)
        .copy(offset=skip, limit=limit)
        .execute(exhaust_results=False)
    )

    # Get total count
    total = (
        await redis_client.ft(config.index_name).search(
            search_index.count_query(years=years, categories=categories)
        )
    ).total

    total = 9
    return {"total": total, "papers": papers}


@r.post("/vectorsearch/text", response_model=Dict)
async def find_papers_by_paper_id(similarity_request: SimilarityRequest) -> Dict:
    # Create query
    query = search_index.vector_query(
        similarity_request.categories,
        similarity_request.years,
        similarity_request.search_type,
        similarity_request.number_of_results,
    )
    count_query = search_index.count_query(
        years=similarity_request.years, categories=similarity_request.categories
    )

    # find the vector of the Paper listed in the request
    paper_vector_key = "THM:Paper:" + str(similarity_request.paper_id)
    vector = await redis_client.hget(paper_vector_key, "vector")

    # obtain results of the queries
    total, results = await asyncio.gather(
        redis_client.ft(config.index_name).search(count_query),
        redis_client.ft(config.index_name).search(
            query, query_params={"vec_param": vector}
        ),
    )

    # Get Paper records of those results
    return await papers_from_results(total.total, results)


@r.post("/vectorsearch/text/user", response_model=Dict)
async def find_papers_by_user_text(
    similarity_request: UserTextSimilarityRequest,
) -> Dict:
    # Create query
    query = search_index.vector_query(
        similarity_request.categories,
        similarity_request.years,
        similarity_request.search_type,
        similarity_request.number_of_results,
    )
    count_query = search_index.count_query(
        years=similarity_request.years, categories=similarity_request.categories
    )

    # obtain results of the queries
    total, results = await asyncio.gather(
        redis_client.ft(config.index_name).search(count_query),
        redis_client.ft(config.index_name).search(
            query,
            query_params={
                "vec_param": embeddings.make(similarity_request.user_text).tobytes()
            },
        ),
    )

    # Get Paper records of those results
    return await papers_from_results(total.total, results)
