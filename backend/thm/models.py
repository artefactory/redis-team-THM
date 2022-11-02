from aredis_om import Field, HashModel


class Paper(HashModel):
    paper_id: str
    title: str = Field(index=True, full_text_search=True)
    authors: str
    abstract: str = Field(index=True, full_text_search=True)
    categories: str = Field(index=True)
    category_weights: str  # TODO: add Tom's category_weights (1, see below)
    year: str = Field(index=True)
    # vector: bytes


# (1) add Tom's weight categories in a '|' separed string instead of normal list
# in fact, just like for the categories subfield,
# Redis can't store Lists in subfields in general, that why we use string to encode this

# FIXME Doesn't work with pydantic
# File "pydantic/json.py", line 45, in pydantic.json.lambda
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe2 in position 0: invalid continuation byte
