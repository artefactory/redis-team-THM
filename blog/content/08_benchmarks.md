Title: TODO
Date: 2022-10-30 12:05
Modified: 2022-10-30 12:05
Category: MLOps
Tags: redis
Slug: cost-stack
Authors: Michel Hua
Summary: TODO

_Day 8 - When we ran some benchmark for the process of index creation and hosting._

# The Cost of the Stack

https://mlops.community/vector-similarity-search-from-basics-to-production/

pricing of the stack

From a file named `arxiv-metadata-oai-snapshot.json` containing metadata and abstracts of aout 2M papers in 153 different scientific categories, we generated partial indexes and evaluated how it can run in production considering:

- machine provisining needed,
- how to update regularly from the arXiv snapshots,
- volumetry of data.

### Generating Embeddings

First, we evaluated the Jupyter notebooks from Redis demo code [`RedisVentures/redis-arXiv-search`](https://github.com/RedisVentures/redis-arXiv-search/tree/main/data).

| Model                    | Machine                      | Time   |
|-------------------------:|------------------------------|-------:|
|            `arxiv-embeddings.ipynb` | [Apple M1 Pro 8-core](https://www.apple.com/macbook-pro-14-and-16/specs/) | 17min |
|            `arxiv-embeddings.ipynb` | [Saturn Cloud T4-XLarge 4-cores](https://saturncloud.io/plans/hosted/) | 4min |
| `single-gpu-arxiv-embeddings.ipynb` | T4-XLarge 4-cores, `saturn-python-rapids` image | 30min |

### Loading Index on Redis Cloud

| Model                    | Machine                      | Time   |
|-------------------------:|------------------------------|-------:|
| `arxiv_embeddings_10000.pkl` | [Apple M1 Pro 8-core](https://www.apple.com/macbook-pro-14-and-16/specs/) | 6min |

# Profiling the code

Using [`pythonprofilers/memory_profiler`](https://github.com/pythonprofilers/memory_profiler) we measured that,



### Load testing the HTTP Server

Using [`wg/wrk`](https://github.com/wg/wrk)

```sh
$ wrk -t4 -c20 -d30s https://thm-cli.community.saturnenterprise.io/api/docs

Running 30s test @ https://thm-cli.community.saturnenterprise.io/api/docs
  4 threads and 20 connections

  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   105.53ms   21.50ms 461.06ms   88.24%
    Req/Sec    47.63      7.97    80.00     79.85%
  5629 requests in 30.11s, 5.74MB read
Requests/sec:    186.98
Transfer/sec:    195.19KB
```