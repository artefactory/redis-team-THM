from enum import Enum
from typing import List, Optional, Tuple, Union

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
    categories: Union[str, List[Tuple[str, str]]]
    predicted_categories: Optional[Union[str, List[str]]]
    year: str
