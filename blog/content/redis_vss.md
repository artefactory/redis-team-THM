Title: Redis Vector Similarity Search
Date: 2022-10-28 11:00
Modified: 2022-10-28 11:00
Category: Technology
Tags: redis
Slug: redis-vss
Authors: Tom Darmon, Henrique Brito, Michel Hua
Summary: Redis Vector Similarity Search

## About Vector Similarity

...

### Solutions for using it in production

In 2015, Spotify was one of the first large Internet company to use these algorithms in production and Erik Bernhardsson open sourced `annoy` at that time.

```
TODO write more about the history and whas Facebook provides with their library
What are the achievements of Google Cloud Platform.
```

## Redis Vector Similarity Search

Few words about RedisSearch

![VSS](https://redis.com/wp-content/uploads/2022/05/rediscover-redis-for-vector-similarity-search-similarity-searches-1024x580.png?&auto=webp&quality=85,75&width=1200)

https://gist.github.com/mycaule/fcc307228b3b0bc80ee322949463435b

:::python
    if config.index_type == "HNSW":
        await search_index.create_hnsw(
            categories_field,
            year_field,
            redis_conn=redis_conn,
            number_of_vectors=len(papers),
            prefix="THM:Paper:",
            distance_metric="IP",
            vector_size=vector_size,
        )
    else:
        await search_index.create_flat(
            categories_field,
            year_field,
            redis_conn=redis_conn,
            number_of_vectors=len(papers),
            prefix="THM:Paper:",
            distance_metric="IP",
            vector_size=vector_size,
        )

> https://redis.io/docs/stack/search/reference/vectors/

## Getting started with Redis Cloud Enterprise

### Configure your Account

https://gist.github.com/mycaule/7bdb23dbaa63fd7223450332e30a7faa

### Install Redis Insights

...

## References

- [Rediscover Redis for Vector Similarity Search](https://redis.com/blog/rediscover-redis-for-vector-similarity-search/)
- [RedisDays New York 2022 - Using AI to Reveal Trading Signals Buried in Corporate Filings](https://www.youtube.com/watch?v=_Lrbesg4DhY)
- [MLOps Community - e-lab kickoff](www.youtube.com/watch?v=uS9ZGi8RyPM)
- [Ed Sandoval LinkedIn page](https://www.linkedin.com/in/edsandovaluk/)
- [TFHub - Cross-Lingual Similarity and Semantic Search Engine with TF-Hub Multilingual Universal Encoder](https://colab.research.google.com/github/tensorflow/hub/blob/master/examples/colab/cross_lingual_similarity_with_tf_hub_multilingual_universal_encoder.ipynb)
- [Vertex AI - Matching Engine ANN service overview](https://cloud.google.com/vertex-ai/docs/matching-engine/ann-service-overview)
- [Erik Bernahardsson - Approximate nearest neighbors & vector models](https://www.slideshare.net/erikbern/approximate-nearest-neighbor-methods-and-vector-models-nyc-ml-meetup) | [`spotify/annoy`](https://github.com/spotify/annoy)
- [Faiss: A library for efficient similarity search](https://engineering.fb.com/data-infrastructure/faiss-a-library-for-efficient-similarity-search/) | [`facebookresearch/faiss`](https://github.com/facebookresearch/faiss)
- [`perone/euclidesdb`](https://github.com/perone/euclidesdb)
