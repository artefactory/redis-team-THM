Title: Day 5 - Redis Vector Similarity Search
Date: 2022-10-26 16:00
Modified: 2022-10-26 16:00
Category: Technology
Tags: redis
Slug: redis-vss
Authors: Tom Darmon, Henrique Brito, Michel Hua
Summary: Day 5 - Redis Vector Similarity Search

_On Day 5 we investigated the problem of similarity search_

# State of the Art

In 2015, Spotify was one of the first large Internet company to use these algorithms in production and Erik Bernhardsson open sourced [`spotify/annoy`](https://github.com/spotify/annoy) at that time.

In 2017, Facebook then released [`facebookresearch/faiss`](https://github.com/facebookresearch/faiss) to enable searching multimedia documents that are similar to each other, indexing a record of billions of document using GPU

Other open source projects such as [`perone/euclidesdb`](https://github.com/perone/euclidesdb) then enabled developers to use the embeddings comparision concepts to be hosted on a database.

Then BERT models began to outperform most of the models, introducing a new era for NLP. In 2020, GCP also proposed a similarity using Apache Beam and Annoy, which later got refactored to VertexAI.

HuggingFace and OpenAI then largely disrupted access to deep learning models and made it easier to use.

# Redis Vector Similarity Search

Redis Vector Similarity Search (VSS) is an extension in the continuity of the previous backend software technologies, allowing users already familiar with Redis to perform vector similarity queries using `FT.SEARCH` command.

Developers car easily load, index, and query vectors.

![VSS](https://redis.com/wp-content/uploads/2022/05/rediscover-redis-for-vector-similarity-search-similarity-searches-1024x580.png?&auto=webp&quality=85,75&width=1200)

HNSW vs FLAT vectors
> https://redis.io/docs/stack/search/reference/vectors/

# References

## State of the Art of Similarity Search

- [Erik Bernahardsson - Approximate nearest neighbors & vector models](https://www.slideshare.net/erikbern/approximate-nearest-neighbor-methods-and-vector-models-nyc-ml-meetup)
- [Faiss: A library for efficient similarity search](https://engineering.fb.com/data-infrastructure/faiss-a-library-for-efficient-similarity-search/)
- [GCP - Building a real-time embeddings similarity matching system](https://web.archive.org/web/20210307210915/https://cloud.google.com/solutions/machine-learning/building-real-time-embeddings-similarity-matching-system)
- [Vertex AI - Matching Engine ANN service overview](https://cloud.google.com/vertex-ai/docs/matching-engine/ann-service-overview)

## Redis VSS talks

- [Rediscover Redis for Vector Similarity Search](https://redis.com/blog/rediscover-redis-for-vector-similarity-search/)
- [RedisDays New York 2022 - Using AI to Reveal Trading Signals Buried in Corporate Filings](https://www.youtube.com/watch?v=_Lrbesg4DhY)
