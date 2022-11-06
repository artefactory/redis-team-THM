Title: Benchmarks
Date: 2022-10-30 12:05
Modified: 2022-10-30 12:05
Category: MLOps
Tags: redis
Slug: cost-stack
Authors: Michel Hua
Summary: Benchmarks

_Day 8 - When we ran some benchmark for the process of index creation and hosting._

# Benchmarking the loading scripts

From a file named `arxiv-metadata-oai-snapshot.json` containing metadata and abstracts of aout 2M papers in 153 different scientific categories, we generated partial indexes and evaluated how it can run in production considering:

- machine provisining needed,
- how to update regularly from the arXiv snapshots,
- volumetry of data.

## Generating Embeddings

First, we evaluated the Jupyter notebooks from Redis demo code [`RedisVentures/redis-arXiv-search`](https://github.com/RedisVentures/redis-arXiv-search/tree/main/data).

| Model                    | Machine                      | Time   |
|-------------------------:|------------------------------|-------:|
|            `arxiv-embeddings.ipynb` | [Apple M1 Pro 8-core](https://www.apple.com/macbook-pro-14-and-16/specs/) | 17min |
|            `arxiv-embeddings.ipynb` | [Saturn Cloud T4-XLarge 4-cores](https://saturncloud.io/plans/hosted/) | 4min |
| `single-gpu-arxiv-embeddings.ipynb` | T4-XLarge 4-cores, `saturn-python-rapids` image | 30min |

To then load the Pickle index to Redis is easy from a normal desktop machine.

| Model                    | Machine                      | Time   |
|-------------------------:|------------------------------|-------:|
| `arxiv_embeddings_10000.pkl` | [Apple M1 Pro 8-core](https://www.apple.com/macbook-pro-14-and-16/specs/) | 6min |

## Profiling the code

After refactoring to Python scripts, we used [`Delgan/loguru`](https://github.com/Delgan/loguru) to add logs, [`tqdm/tqdm`](https://github.com/tqdm/tqdm) to track troughput and [`pythonprofilers/memory_profiler`](https://github.com/pythonprofilers/memory_profiler) to find pain points and we measured that,

```sh
$ python3 -m memory_profiler generate_index.py \
  --year_month=200811 \
  --input_path="arxiv-metadata-oai-snapshot.json" \
  --output_path="arxiv/cutoff=200811/output.pkl" \
  --model_name="sentence-transformers/all-MiniLM-L12-v2"
```

As we can see using `pandas` to load and store data wasn't optimal because of its memory overhead.

```sh
$ python3 -m memory_profiler load_data.py \
  --concurrency_level=2 \
  --separator="|"  \
  --vector_size=384 \
  --reset_db=False \
  --embeddings_path="arxiv/cutoff=200811/output.pkl"

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    98     67.0 MiB     67.0 MiB           1   @profile
    99                                         def run(
   ...
   107
   108     67.2 MiB      0.2 MiB           1       config = get_settings()
   109
   110     67.2 MiB      0.0 MiB           1       if reset_db:
   111                                                 logger.info(f"TODO {reset_db}")
   112
   113     67.2 MiB      0.0 MiB           2       Paper.Meta.database = get_redis_connection(
   114     67.2 MiB      0.0 MiB           1           url=config.get_redis_url(), decode_responses=True
   115                                             )
   116     67.2 MiB      0.0 MiB           1       Paper.Meta.global_key_prefix = "THM"
   117     67.2 MiB      0.0 MiB           1       Paper.Meta.model_key_prefix = "Paper"
   118
   119     67.2 MiB      0.0 MiB           1       redis_conn = redis.from_url(config.get_redis_url())
   120
   121    165.1 MiB     97.8 MiB           2       asyncio.run(
   122     67.2 MiB      0.0 MiB           2           load_all_data(
   ...


    51   67.969 MiB   67.969 MiB           1   @profile
    52                                         async def load_all_data(
   ...
    62   67.984 MiB    0.016 MiB           1       logger.info("Loading papers...")
    63  607.562 MiB  539.578 MiB           1       papers = read_paper_df(embeddings_path).head(1)
    64  152.219 MiB -455.344 MiB           1       papers = papers.to_dict("records")
    65
    66  152.219 MiB    0.000 MiB           1       logger.info("Writing to Redis...")
    67  152.578 MiB  304.844 MiB           4       await gather_with_concurrency(
    68  152.219 MiB    0.000 MiB           2           redis_conn, concurrency_level, separator, vector_size, *papers
```

# Load testing the HTTP Server

Using [`wg/wrk`](https://github.com/wg/wrk) we have made a few tests to see how much HTTP server and Redis could handle if many clients connected to it.

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

```sh
$ wrk -t4 -c10 -d30s --script benchmark/post_similar.lua https://thm-cli.community.saturnenterprise.io/api/v1/paper/vectorsearch/text
Running 30s test @ https://thm-cli.community.saturnenterprise.io/api/v1/paper/vectorsearch/text
  4 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   352.05ms   52.12ms 697.77ms   89.43%
    Req/Sec     5.96      2.66    10.00     50.36%
  672 requests in 30.04s, 12.83MB read
Requests/sec:     22.37
Transfer/sec:    437.32KB
```

```sh
$ wrk -t4 -c10 -d30s --script benchmark/post_text.lua https://thm-cli.community.saturnenterprise.io/api/v1/paper/vectorsearch/text/user
Running 30s test @ https://thm-cli.community.saturnenterprise.io/api/v1/paper/vectorsearch/text/user
  4 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   575.41ms  171.71ms   1.48s    89.46%
    Req/Sec     4.16      3.14    10.00     58.23%
  408 requests in 30.06s, 8.60MB read
Requests/sec:     13.57
Transfer/sec:    292.92KB
```

# Discussing the Cost of Hosting

Pricing of the stack

- Redis Cloud Enterprise: $0.881/hr = USD 600/month
- Saturn Cloud Notebooks and Deployment: $0.21/hour = USD 150/month

The total is about 750 USD/month. You might be able to decrease costs a bit using infrastructure as a service instead of platform as a service, but more DevOps skills would be needed to configure cloud accounts on GCP or AWS for example.
