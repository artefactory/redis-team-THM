#!/usr/bin/python3

from prompt_toolkit import prompt, print_formatted_text as print
import httpx
from helpers.models import Paper


def format_response(paper):
    resp = { your_key: paper[your_key] for your_key in ['title', 'authors', 'categories', 'year'] }
    resp ['url'] = f"https://arxiv.org/pdf/{paper['paper_id']}.pdf"
    return resp


# https://www.bibtex.com/e/article-entry/
def bibtex(paper: Paper):
    res =f"""@article{{{paper.authors[:5].replace(" ", "").lower()}{paper.year[2:]},
    author = {paper.authors},
    title = {paper.title},
    year = {paper.year},
    url = {paper.url},
    abstract = ...,
    keywords = ...
}}"""
    return res


print("THM Search CLI, your arXiv-Bibtex helper")

base_url = "https://docsearch.redisventures.com/api/v1/paper"

user_text = prompt("Enter a search query to discover scholarly papers: ")
years = prompt("What year: ")

data = {
    "user_text": user_text,
    "search_type": "KNN",
    "number_of_results": 3,
    "years": [],
    "categories": [],
}

resp = httpx.post(f"{base_url}/vectorsearch/text/user", json=data).json()
resp2 = list(map(format_response, resp["papers"]))

print("'''")
for r in list(map(format_response, resp["papers"])):
    print(bibtex(Paper.parse_obj(r)))
print("'''")

# 'pk', 'paper_id', 'title', 'authors', 'abstract', 'categories', 'year', 'input', 'similarity_score'

print(f"Total of {resp['total']:,d} searchable arXiv papers. Last updated 2022-11-04.")
