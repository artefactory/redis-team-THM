#!/usr/bin/python3

import webbrowser
from typing import List

from helpers.category_parser import parse_categories_from_redis
from helpers.models import Format, Paper
from helpers.quotes import random_quote
from helpers.search_engine import SearchEngine
from helpers.settings import Settings
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter, WordCompleter
from question_answering import get_answer_to_prompt

from loguru import logger

def _BibTeX(paper: Paper):
    """Renders to BibTeX format"""
    # https://www.bibtex.com/e/article-entry/
    return f"""@article{{{paper.authors[:5].replace(" ", "").lower()}{paper.year[2:]}, \t % {", ".join(f"{x[0]} {x[1]}".strip() for x in paper.categories)}
    author = "{paper.authors}",
    title = "{paper.title}",
    year = "{paper.year}",
    url = "{paper.url}",
}}"""


def _Mardown_header():
    return """| author | title | year | url | keywords |
|--------|-------|------|-----|----------|"""


def _Markdown(paper: Paper):
    """Renders to Markdown table format."""
    # https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables
    return f"| {paper.authors} | {paper.title} | {paper.year} | {paper.url} | ... |"


def render_results(papers: List[Paper], format: Format = Format.BibTeX):
    print()
    if format == Format.BibTeX:
        print("```bibtex")
        for p in papers:
            print(_BibTeX(p))
    elif format == Format.Markdown:
        print("```txt")
        print(_Mardown_header())
        for p in papers:
            print(_Markdown(p))
    else:
        return

    print("```")
    print()
    paper_ids = list(map(lambda x: x.paper_id, papers))
    print("To go further, use 'search similar', 'search details' commands...")
    print(HTML(f"with these arXiv IDs as reference <b>{paper_ids}</b>"))
    print()


def render_paper(paper: Paper):
    clean_title = paper.title.replace("\n", "").replace("  ", " ")
    clean_authors = paper.authors.replace("\n", "").replace("  ", " ")
    print(HTML(f"<b>{clean_title}</b>"))
    print(f"by {clean_authors}")
    print("=" * 80)
    print("Categories:")
    print("", *parse_categories_from_redis(paper.categories))
    print("=" * 80)
    print(paper.abstract)
    print()


def goto_search_keywords():
    print("Enter a search query to discover scholarly papers.")
    user_text = ps.prompt(
        "Your keywords (eg. social networks): ",
        auto_suggest=AutoSuggestFromHistory(),
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
    print(f"Opening {paper_id} on arXiv...")
    webbrowser.open(f"https://arxiv.org/pdf/{paper_id}.pdf")
    print()


def goto_wolfram():
    wolfram_query = ps.prompt(
        "Find a formula (eg. cosine law): ", auto_suggest=AutoSuggestFromHistory()
    )
    print()
    print(f"Asking Wolfram Alpha about {wolfram_query}...")
    webbrowser.open(Engine.ask_wolfram(wolfram_query))
    print()


def goto_stackexchange():
    so_query = ps.prompt("Write your question: ", auto_suggest=AutoSuggestFromHistory())
    print()
    print(f"Asking StackExchange about {so_query}...")
    webbrowser.open(Engine.ask_stackexchange(so_query))
    print()


def goto_configure():
    format_choice = ps.prompt(
        "Choose file format (markdown, bibtex): ",
        completer=WordCompleter(["markdown", "bibtex"]),
    )
    settings.format = Format(format_choice)

    max_results_choice = ps.prompt("Max Results (eg. 3): ")
    settings.max_results = max_results_choice
    print()


def goto_find_answer():
    print()
    print(
        "This is a beta feature! Ask question and we will look for the article that seems to answer it best."
    )
    user_prompt = ps.prompt(
        "Ask what is on your mind: ", auto_suggest=AutoSuggestFromHistory()
    )

    print(
        HTML(
            "<seagreen>We're looking for your answer. This can take a minute...</seagreen>"
        )
    )

    answers = get_answer_to_prompt(Engine, user_prompt, top_k=1)
    for answer, confidence, paper in answers:
        # get similar papers to display
        print()
        print("-" * 80)
        print(f"I am {confidence:.0%} sure about my answer:")
        print(HTML(f"Answer: <b>'{answer}'</b>"))
        print()
        print("This answer came from here:")
        render_paper(paper)


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
            "stackexchange": None,
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
        goto_find_answer()
        goto_menu()
    elif menu_choice == "find formula":
        goto_wolfram()
        goto_menu()
    elif menu_choice == "find stackexchange":
        goto_stackexchange()
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

Engine = SearchEngine("https://thm-cli.community.saturnenterprise.io/api/v1/paper")
# Engine = SearchEngine("https://docsearch.redisventures.com/api/v1/paper")
# Engine = SearchEngine("http://localhost:8080/api/v1/paper")

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
