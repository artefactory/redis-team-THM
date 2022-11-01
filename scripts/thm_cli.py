#!/usr/bin/python3

from typing import List
from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import prompt

from helpers.models import Paper
from helpers.search_engine import SearchEngine

from loguru import logger

# https://www.bibtex.com/e/article-entry/
def BibTeX(paper: Paper):
    return f"""@article{{{paper.authors[:5].replace(" ", "").lower()}{paper.year[2:]},
    author = {paper.authors},
    title = {paper.title},
    year = {paper.year},
    url = {paper.url},
    abstract = ...,
    keywords = ...
}}"""


def print_BibTeX(papers: List[Paper]):
    print()
    print("'''")
    for p in papers:
        print(BibTeX(p))
    print("'''")


print(HTML("<b><skyblue>THM Search CLI</skyblue>, your arXiv-BibTeX helper</b>"))
print()
print()

print("Enter a search query to discover scholarly papers.")
user_text = prompt("Your keywords: ")
# years = prompt("What year: ")
# categories = prompt("What categories: ")

Engine = SearchEngine("https://docsearch.redisventures.com/api/v1/paper")

search_papers, total = Engine.search(user_text)
print(HTML(f'<seagreen>Papers matching "{user_text}"...</seagreen>'))
print_BibTeX(search_papers)

paper_id = "2006.12278"
similar_papers, _ = Engine.similar_to(paper_id)
print(HTML(f"<seagreen>Papers similar to {paper_id}...</seagreen>"))
print_BibTeX(similar_papers)

print(HTML(f'<seagreen>Retrieving details for "{paper_id}"...</seagreen>'))
paper_id = "2006.12278"
paper = Engine.paper(paper_id)

print(paper.title)
print("=" * 80)
print(paper.abstract)

print(f"Total of {total:,d} searchable arXiv papers. Last updated 2022-11-04.")
