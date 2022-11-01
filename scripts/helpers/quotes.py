import random

from pydantic import BaseModel


class Quote(BaseModel):
    sentence: str
    author: str


QUOTES = [
    Quote(
        sentence="A mathematician is a device for turning coffee into theorems.",
        author="Paul Erdos",
    ),
    Quote(
        sentence="Games are won by players who focus on the playing field, not by those whose eyes are glued to the scoreboard.",
        author="Warren Buffet",
    ),
    Quote(
        sentence="I thought dynamic programming was a good name.\nIt was something not even a Congressman could object to.\nSo I used it as an umbrella for my activities.",
        author="Richard Bellman",
    ),
    Quote(
        sentence="The single most important thing in life is to believe in yourself regardless of what everyone else says.",
        author="Hikaru Nakamura",
    ),
]


def random_quote():
    return random.choice(QUOTES)
