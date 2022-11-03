from enum import Enum
from typing import Optional

from pydantic import BaseModel


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
    predicted_categories: Optional[str]
    year: str
