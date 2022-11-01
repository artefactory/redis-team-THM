from pydantic import BaseModel


<<<<<<< Updated upstream
=======
class Format(str, Enum):
    BibTeX = "bibtex"
    Markdown = "markdown"


>>>>>>> Stashed changes
class Paper(BaseModel):
    url: str
    title: str
    authors: str
    categories: str
    year: str