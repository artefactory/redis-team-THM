from pydantic import BaseModel


class Paper(BaseModel):
    url: str
    title: str
    authors: str
    categories: str
    year: str