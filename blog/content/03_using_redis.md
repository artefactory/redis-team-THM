Title: Day 3 - Using Redis
Date: 2022-10-23 10:20
Modified: 2022-10-23 10:20
Category: Technology
Tags: redis
Slug: using-redis
Authors: Michel Hua
Summary: Day 3 - The most common uses of Redis

_On day 3, just a few days before the start of the Hackathon, what we did is learn about Redis._

# What can I do with Redis?

Redis is an open source in memory NoSQL database that was created in 2009.

When you already have a database like MongoDB, SQL Server, MySQL, and parts of your website or your application need to get data quicker than your database can, Redis is usually the go for solution.

This is achieved by hosting part of the data in memory as a cache, as opposite to traditional databases which would use disk.

Some of its use cases are:

- storing sessions in Redis,
- keeping lists of most recent visitors,
- describing your contacts or friends graph,
- implementing real-time workflows with the pub/sub pattern.

Redis enables web developers to build scalable interactive applications. It is used by large companies such as _Twitter_, _Instagram_, _Pinterest_, _StackOverflow_ or _GitHub_.

To get started with Redis, you can just visit,

- [Redis website](https://redis.io/)
- [`redis/redis`](https://github.com/redis/redis)

If you prefer managed services, these are some modern solutions for your production application:

- [Redis Cloud Enterprise](https://redis.com/redis-enterprise-cloud/overview/)
- [Amazon ElasticCache](https://aws.amazon.com/redis/)
- [Azure Cache for Redis](https://azure.microsoft.com/en-us/products/cache/)
- [GCP Memorystore](https://cloud.google.com/memorystore/)

# Redis in Details

Traditional key/value store only handle string type values. Redis is what we call a key/data structures store. This makes it relate more to a database. The different data types it can handle are: strings, lists, sets, sorted sets, hash, Bitmaps, HyperLogLogs.

Redis is very fast for both reads and writes because it runs in memory, while having disk persistence as a backup.
It can run in clusters of servers where large amounts of memory are available.

# Using Redis

Redis can be used a cache and as a second database. Redis helps you scale while keeping in memory the data retrieved from the database.

On some cases, it can be used as a primary database, for example in use cases where only the fresh data matters and when it is only necessary to keep it small periods of time as in streaming.

It can be useful for the Pub/Sub patterns when Internet users have their browsers open, and data is sent automatically without them to refresh the page.

Because of its single threaded nature, it has no lock, and can respond to the load of many requests.

With high-speed data, where you're trying to keep your website responding for things that traditional databases were not initially designed for.

## Using with Python

The Python package [`redis-om`](https://github.com/redis/redis-om-python) is an ORM to interact with the Redis database, it uses [`pydantic`](https://github.com/pydantic/pydantic) to describe your data models and eases operations for modeling and querying data in Redis with modern Python applications.

Another interesting library is [`brainix/pottery`](https://github.com/brainix/pottery) if you want to deal with remote data structures when your application need to implement locks, key value stores, maintain user lists such as e-commerce carts.

## Using the REDIS prompt

Here are some command to manipulate Hashes in Redis,

### [`HGET`](https://redis.io/commands/hget/)

This command can be used to retrieve fields from a specific key.

```txt
> HGET THM:Paper:1609.05486 paper_id
"1609.05486"

> HGET THM:Paper:1609.05486 authors
"M. Kachouane (USTHB), S. Sahki, M. Lakrouf (CDTA, USTHB), N. Ouadah\n  (CDTA)"
```

### [`FT.SEARCH`](https://redis.io/commands/ft.search/)

This command can be used to search index with a textual query.

```txt
...
```

### [`FLUSHDB`](https://redis.io/commands/flushdb/)

This command can be used to delete all keys from a database.

```txt
> FLUSHDB
```

# Redis Stack and RediSearch

Redis provides a modern extension that enables querying, indexing and full-text search.

Among other features, RediSearch support multi-field queries, aggregation, exact phrase matching, numeric filtering, geo filtering and vector similarity semantic search on top of text queries.

# References

- [Josiah L. Carlson - Redis in Action](https://www.goodreads.com/book/show/16033444-redis-in-action)
- [PyData Seattle 2015 - Top 5 uses of Redis as a Database](https://www.youtube.com/watch?v=jTTlBc2-T9Q)
- [Redis Stack - RediSearch](https://redis.io/docs/stack/search/)