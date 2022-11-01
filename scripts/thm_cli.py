#!/usr/bin/python3

from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import prompt

from helpers.models import Paper
from helpers.query_engine import QueryEngine


# https://www.bibtex.com/e/article-entry/
def Bibtex(paper: Paper):
    return f"""@article{{{paper.authors[:5].replace(" ", "").lower()}{paper.year[2:]},
    author = {paper.authors},
    title = {paper.title},
    year = {paper.year},
    url = {paper.url},
    abstract = ...,
    keywords = ...
}}"""


print(HTML("<b><skyblue>THM Search CLI</skyblue>, your arXiv-Bibtex helper</b>"))
print()

user_text = prompt("Enter a search query to discover scholarly papers: ")
years = prompt("What year: ")
categories = prompt("What categories: ")

Engine = QueryEngine("https://docsearch.redisventures.com/api/v1/paper")

papers, total = Engine.make_text_request(user_text)

print("'''")
for p in papers:
    print(Bibtex(p))
print("'''")


print(f"Total of {total:,d} searchable arXiv papers. Last updated 2022-11-04.")
