from aredis_om import Field, HashModel


class Paper(HashModel):
    paper_id: str
    title: str = Field(index=True, full_text_search=True)
    authors: str
    abstract: str = Field(index=True, full_text_search=True)
    categories: str = Field(index=True)
    year: str = Field(index=True)


class Embedding(HashModel):
    paper_pk: str
    paper_id: str
    categories: str
    year: str
    vector: bytes
