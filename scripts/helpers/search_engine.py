from typing import List, Tuple

import httpx
from loguru import logger

from helpers.models import Paper
from urllib.parse import quote

class SearchEngine:
    def __init__(self, base_uri: str):
        self.base_uri = base_uri

    @staticmethod
    def __format_response(paper) -> Paper:
        resp = {
            key: paper[key]
            for key in ["paper_id", "title", "authors", "categories", "year"]
        }
        resp["authors"] = resp["authors"].replace("\n", "").replace("  ", " ")
        resp["title"] = resp["title"].replace("\n", "").replace("  ", " ")
        resp["url"] = f"https://arxiv.org/pdf/{paper['paper_id']}.pdf"
        return Paper.parse_obj(resp)

    def search(self, user_text: str, max_results=3) -> Tuple[List[Paper], int]:
        data = {
            "user_text": user_text,
            "search_type": "KNN",
            "number_of_results": max_results,
            "years": [],
            "categories": [],
        }

        resp = httpx.post(f"{self.base_uri}/vectorsearch/text/user", json=data).json()
        # Available fields
        # pk, paper_id, title, authors, abstract, categories, year, input, similarity_score

        return list(map(self.__format_response, resp["papers"])), resp["total"]

    def similar_to(
        self, paper_id: str, max_results=3, min_score=0
    ) -> Tuple[List[Paper], int]:
        data = {
            "paper_id": paper_id,
            "search_type": "KNN",
            "number_of_results": max_results,
            "years": [],
            "categories": [],
        }
        resp = httpx.post(f"{self.base_uri}/vectorsearch/text", json=data).json()

        # TODO filter min_score
        return list(map(self.__format_response, resp["papers"])), resp["total"]

    def paper(self, paper_id: str) -> str:
        data = {
            "paper_id": paper_id,
            "search_type": "KNN",
            "number_of_results": 1,
            "years": [],
            "categories": [],
        }
        resp = httpx.post(f"{self.base_uri}/vectorsearch/text", json=data).json()

        if "papers" in resp and resp["papers"][0]["paper_id"] == paper_id:
            return Paper.parse_obj(resp["papers"][0])

    def ask_wolfram(self, query: str) -> str:
        return f"https://www.wolframalpha.com/input?i={quote(query)}"
