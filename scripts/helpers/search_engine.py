import re
from typing import List, Tuple
from urllib.parse import quote

import httpx
from loguru import logger

from helpers.models import Paper


class SearchEngine:
    def __init__(self, base_uri: str):
        self.base_uri = base_uri

    @staticmethod
    def __format_response(paper) -> Paper:
        resp = {
            key: paper[key]
            for key in ["paper_id", "title", "authors", "year"]
        }

        # if "predicted_categories" in paper and paper["predicted_categories"]:
        #     arr = paper["predicted_categories"].split("|")
        #     arr = list(map(lambda x: re.findall(r'([\w.]+)\(([\w.]+)\)', x)[0], arr))
        #     resp["categories"] = list(map(lambda x: (x[0], "⭐️"*int(float(x[1])*10)), arr))
        # else:
        #     arr = paper["categories"].split(",")
        #     resp["categories"] = list(map(lambda x: (x, ""), arr))

        if "predicted_categories" in paper and paper["predicted_categories"]:
            resp["predicted_categories"] = paper["predicted_categories"]

        resp["categories"] = list(
            map(lambda x: (x, ""), paper["categories"].split(","))
        )
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
            "number_of_results": 15,
            "years": [],
            "categories": [],
        }

        r = httpx.post(f"{self.base_uri}/vectorsearch/text", json=data)

        if r.status_code == 200:
            resp = r.json()

            if "papers" in resp:
                return Paper.parse_obj(resp["papers"][0])

    def ask_wolfram(self, query: str) -> str:
        return f"https://www.wolframalpha.com/input?i={quote(query)}"

    def ask_stackexchange(self, query: str) -> str:
        return f"https://stackexchange.com/search?q={quote(query)}"
