from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Format(str, Enum):
    BibTeX = "bibtex"
    Markdown = "markdown"


class Paper(BaseModel):
    url: Optional[str]
    paper_id: str
    title: str
    abstract: Optional[str]
    authors: str
    categories: str
    year: str
