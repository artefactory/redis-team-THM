from typing import List, Tuple

import httpx

from helpers.models import Paper


class QueryEngine:
    def __init__(self, base_uri: str):
        self.base_uri = base_uri

    @staticmethod
    def _format_response(paper) -> Paper:
        resp = {key: paper[key] for key in ["title", "authors", "categories", "year"]}
        resp["url"] = f"https://arxiv.org/pdf/{paper['paper_id']}.pdf"
        return Paper.parse_obj(resp)

    def make_text_request(
        self, user_text: str, max_results=3
    ) -> Tuple[List[Paper], int]:
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

        return list(map(self._format_response, resp["papers"])), resp["total"]
