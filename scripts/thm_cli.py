#!/usr/bin/python3

import webbrowser
from typing import List

from loguru import logger
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter, WordCompleter
from prompt_toolkit.history import FileHistory, InMemoryHistory

from helpers.models import Format, Paper
from helpers.quotes import Quote, random_quote
from helpers.search_engine import SearchEngine
from helpers.settings import Settings


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


def render_paper(paper: Paper):
    clean_title = paper.title.replace("\n", "").replace("  ", " ")
    clean_authors = paper.authors.replace("\n", "").replace("  ", " ")
    print(HTML(f"{clean_title}"))
    print(f"by {clean_authors}")
    print("=" * 80)
    print(paper.abstract)
    print()


def goto_search_keywords():
    print("Enter a search query to discover scholarly papers.")
    user_text = ps.prompt(
        "Your keywords (eg. social networks): ", auto_suggest=AutoSuggestFromHistory()
    )
    # years = ps.prompt("What year: ")
    # categories = ps.prompt("What categories: ")
    search_papers, total = Engine.search(user_text, settings.max_results)
    print(HTML(f'<seagreen>Papers matching "{user_text}"...</seagreen>'))
    render_results(search_papers, format=settings.format)
    print(f"Total of {total:,d} searchable arXiv papers. Last updated 2022-11-04.")


def goto_search_similar():
    paper_id = ps.prompt(
        "arXiv ID (eg. 2205.13980): ", auto_suggest=AutoSuggestFromHistory()
    )
    similar_papers, total = Engine.similar_to(paper_id, settings.max_results)
    print(HTML(f"<seagreen>Papers similar to {paper_id}...</seagreen>"))
    render_results(similar_papers, format=settings.format)
    print(f"Total of {total:,d} searchable arXiv papers. Last updated 2022-11-04.")


def goto_search_details():
    paper_id = ps.prompt(
        "arXiv ID (eg. 2205.13980): ", auto_suggest=AutoSuggestFromHistory()
    )
    print(HTML(f"<seagreen>Retrieving details for {paper_id}...</seagreen>"))
    print()
    paper = Engine.paper(paper_id)
    render_paper(paper)
    print("Opening on arXiv...")
    webbrowser.open(f"https://arxiv.org/pdf/{paper_id}.pdf")
    print()


def goto_wolfram():
    wolfram_query = ps.prompt(
        "Find a formula (eg. cosine law): ", auto_suggest=AutoSuggestFromHistory()
    )
    print()
    print("Asking Wolfram Alpha...")
    webbrowser.open(Engine.ask_wolfram(wolfram_query))
    print()


def goto_configure():
    format_choice = ps.prompt(
        "Choose file format (markdown, bibtex): ",
        completer=WordCompleter(["markdown", "bibtex"]),
    )
    settings.format = Format(format_choice)

    max_results_choice = ps.prompt(f"Max Results (current. {settings.max_results}): ")
    settings.max_results = max_results_choice
    print()


def goto_exit():
    print()
    print()
    print("Thank you for using the service!")
    print("Have a good day!")
    print()


menu_completer = NestedCompleter.from_nested_dict(
    {
        "search": {
            "keywords": None,
            "similar": None,
            "details": None,
        },
        "find": {
            "answer": None,
            "formula": None,
        },
        "configure": None,
        "help": None,
        "exit": None,
    }
)


def goto_menu():
    menu_choice = ps.prompt("THM # ", completer=menu_completer)
    if menu_choice == "search keywords":
        goto_search_keywords()
        goto_menu()
    elif menu_choice == "search similar":
        goto_search_similar()
        goto_menu()
    elif menu_choice == "search details":
        goto_search_details()
        goto_menu()
    elif menu_choice == "find answer":
        print("  TODO Henrique")
        goto_menu()
    elif menu_choice == "find formula":
        goto_wolfram()
        goto_menu()
    elif menu_choice == "configure":
        goto_configure()
        goto_menu()
    elif menu_choice == "help":
        print("THM Search CLI v1.0")
        print("https://artefactory.github.io/redis-team-THM")
        print()
        print("Usage:")
        print("  search [keywords|similar|details]")
        print("  find [answer|formula]")
        print("  configure")
        print("  help")
        print("  exit")
        goto_menu()
    elif menu_choice == "exit":
        goto_exit()
    else:
        goto_menu()


print(HTML("<b><skyblue>THM Search CLI</skyblue></b>"))
print(HTML("Your arXiv-BibTeX terminal assistant."))
print()

Engine = SearchEngine("https://docsearch.redisventures.com/api/v1/paper")
ps = PromptSession()
settings = Settings()
quote = random_quote()

print("---")
print(HTML(f"<i>{quote.sentence}</i>"))
print(quote.author)
print("---")
print()
print()

goto_menu()
