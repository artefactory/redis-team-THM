Title: Using Redis
Date: 2022-10-28 10:20
Modified: 2022-10-28 10:20
Category: Technology
Tags: redis
Slug: using-redis
Authors: Michel Hua
Summary: The most common uses of Redis

## What can I do with Redis?

Redis is an open source in memory NoSQL database it was created in 2009.

Redis primary use is when you have a database like MongoDB, SQL server, MySQL, and parts of your website or your application need to get data more quicker than your database can.

You can achieve this by hosting part of the data in memory as a cache in Redis.

Redis can handle data structures such as `Strings`, `Lists`, `Sets`, `Sorted Sets` and `Hashes` and also more advanced one.

Here are some of its use cases:

- storing your sessions in Redis,
- keeping a list of most recent visitors,
- comparing which one of your friends are my friends,
- implementing realtime workflows with the pub/sub pattern.

Redis enables web developpers to build scalable interactive applications. It is used by large companies such as Twitter, Instagram, Pinterest, StackOverflow or GitHub.

To get started with Redis,

- https://redis.io/
- https://github.com/redis/redis

If you prefer managed services, these are some modern solutions for your production application:

- [Redis Cloud Enterprise](https://redis.com/redis-enterprise-cloud/overview/)
- [Amazon ElasticCache](https://aws.amazon.com/redis/)
- [Azure Cache for Redis](https://azure.microsoft.com/en-us/products/cache/)
- [GCP Memorystore](https://cloud.google.com/memorystore/)

## Redis in Details

Traditional key/value store only handle string type values. Redis is what we call a key/data structures store. This makes it relate more to a database. The different data types is can handle are: strings, lists, sets, sorted sets, hash, Bitmaps, HyperLogLogs.

Redis is very fast for both reads and writes because it runs in memory, while having disk persistence as a backup.
It can run in clusters of servers with lots of memory available.

## Using Redis

Redis can be used a cache and as a second database. Redis helps you scale while keeping in memory the data retrieved from the database.

On some cases, it can be used as a primary database, for example in use cases where only the fresh data matters and when it is only necessary to keep it small periods of time as in streaming.

It can be useful for the Pub/Sub patterns when Internet users have their browsers open, and data is sent automatically without them to refresh the page.

Because of its single threaded nature, it has no lock, and can respond the load of many requests.

## Use cases

- Show the most recent items in your application
- Leaderboards that update in realtime
- Show votes and dates for posts
- Expiration dates for shopping carts
- Real time analysis of online activity
- Job queues

With high speed data where you're trying to keep your website responding for things that your database wasn't initially designed for.

## References

- [Josiah L. Carlson - Redis in Action](https://www.goodreads.com/book/show/16033444-redis-in-action)
- [PyData Seattle 2015 - Top 5 uses of Redis as a Database](https://www.youtube.com/watch?v=jTTlBc2-T9Q)