from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Format(str, Enum):
    BibTeX = "bibtex"
    Markdown = "markdown"


class Category(BaseModel):
    name: str
    weight: float   # TODO: add Tom's categories

class Paper(BaseModel):
    url: Optional[str]
    paper_id: str
    title: str
    abstract: Optional[str]
    authors: str
    categories: List[Category]
    year: str
