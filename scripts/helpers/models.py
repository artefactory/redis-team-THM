from pydantic import BaseModel


class Format(str, Enum):
    BibTeX = "bibtex"
    Markdown = "markdown"


class Paper(BaseModel):
    url: str
    title: str
    authors: str
    categories: str
    year: str