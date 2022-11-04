from typing import Optional

from aredis_om import Field, HashModel


class Paper(HashModel):
    paper_id: str = Field(primary_key=True)
    title: str = Field(index=True, full_text_search=True)
    authors: str
    abstract: str = Field(index=True, full_text_search=True)
    categories: str = Field(index=True)
    predicted_categories: Optional[str]
    year: str = Field(index=True)
