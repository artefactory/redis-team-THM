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
    # vector: str


# FIXME Doesn't work with pydantic
# File "pydantic/json.py", line 45, in pydantic.json.lambda
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe2 in position 0: invalid continuation byte
