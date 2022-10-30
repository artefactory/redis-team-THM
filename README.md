# Team THM Submission

<div align="center">
    <img src="backend/thm/data/redis-logo.png" height="25" /> <br />
    <img src="backend/thm/data/artefact-logo.png" height="20" /><br />
    Tom, Henrique, Michel<br />
    Oct. - Nov. 2022
</div>
<br />

[![Netlify Status](https://api.netlify.com/api/v1/badges/d2c3e1e1-fbb6-422a-b44c-848f6753a246/deploy-status)](https://app.netlify.com/sites/sweet-piroshki-f2e396/deploys)

This demo showcases the vector search similarity (VSS) capability within Redis Stack and Redis Enterprise.

Through the RediSearch module, vector types and indexes can be added to Redis.
This turns Redis into a highly performant vector database which can be used for all types of applications.

<details>

![Screen Shot](https://user-images.githubusercontent.com/13009163/191346916-4b8f648f-7552-4910-ad4e-9cc117230f00.png)

</details>

## Documentation

- [Basic Demo](https://docsearch.redisventures.com) | [GitHub](https://github.com/RedisVentures/redis-arXiv-search)
- [Redis Vector Similarity Search](https://redis.io/docs/stack/search/reference/vectors)
- [Huggingface Tokenizers + Models](https://huggingface.co/sentence-transformers)
- [Cornell University - arXiv dataset](https://www.kaggle.com/Cornell-University/arxiv), `arxiv-metadata-oai-snapshot.json` file is used
- [`Buuntu/fastapi-react`](https://github.com/Buuntu/fastapi-react)
- [`FastAPI`](https://fastapi.tiangolo.com/), [`pydantic`](https://pydantic-docs.helpmanual.io/), [`redis-om`](https://redis.io/docs/stack/get-started/tutorials/stack-python/)
- [`react`](https://reactjs.org/), [`react-bootstrap`](https://react-bootstrap.github.io/), [MaterialUI](https://material-ui.com/)
- [`redis`](https://redis.io/docs/stack/) see Vector database and JSON storage
- [Docker Compose](https://docs.docker.com/compose/)

## History

- 15/10 - Added CI/CD script
- 15/10 - Forked from [`RedisVentures/redis-arXiv-search`](https://github.com/RedisVentures/redis-arXiv-search)
- 15/10 - Used Tyler Hutcherson's latest changes: [PR 3](https://github.com/RedisVentures/redis-arXiv-search/pull/3), [PR 9](https://github.com/RedisVentures/redis-arXiv-search/pull/9)

## Machine Setup

```sh
brew install yarn redis docker
pip install backend/requirements.txt
```

## Architecture

<details>

```txt
                        writes pickle and loads index
+-------------------+      +----------------+
|                   |      |                |
|  Redis            +<-----+  Jupyter       |
|                   |      |                |
+--------+----------+      +----------------+
         ^
         |  reads search index
+--------+----------+
|                   |
|  FastAPI          |
|                   |
+--------+----------+
         ^
         |  calls backend
+--------+----------+      +----------------+
|                   |      |                |
|  React            +----->+  arXiv server  |
|                   |      |                |
+-------------------+      +----------------+
            browser use app from here
```

</details>

### TODO

- [x] Setup [Saturn Cloud](https://app.community.saturnenterprise.io/) account
- [x] Setup [Redis Enterprise Cloud](https://redis.com/redis-enterprise-cloud/)
- [x] Setup Blog page and documentation
- [ ] Deploy Backend somewhere, Saturn Cloud ?

## Running The Application

### Run With Docker

```sh
docker compose up
open http://localhost:8888

# To force a new build
docker compose up --build

# To clear Docker cache
docker system prune
```

### Backend Application Only

Setup your Redis Enterprise Cloud then,

```sh
cd backend/
./start.sh

open http://0.0.0.0:8080/api/docs
```

### Frontend Application Only

```sh
cd frontend/
yarn install --no-optional
yarn start
open http://localhost:3000
```

### Exploration

- Trying out [Docarray](https://docarray.jina.ai)

### Blog

```sh
cd blog/

# To preview files locally
pelican content && pelican --listen

# To publish on GitHub pages
pelican content -o output -s pelicanconf.py
ghp-import output -b gh-pages
git push origin gh-pages
```

### Deployment

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://app.netlify.com/start/deploy?repository=https://github.com/artefactory/redis-team-thm)

```sh
yarn global add vercel netlify

# Frontend
netlify build
netlify deploy --prod

# Backend
cd backend
vercel .
```

### Machine Learning Model

First, download the data and run the [`arxiv-embeddings.ipynb`](datascience/arxiv-embeddings.ipynb) notebook to generate some embeddings.

```sh
cd datascience/

pip install sentence_transformers
jupyter run arxiv-embeddings.ipynb

# Uses local CPU and creates embeddings for ~10k machine learning papers.
# input: arxiv-metadata-oai-snapshot.json
# output: arxiv_embeddings_10000.pkl

jupyter run single-gpu-arxiv-embeddings.ipynb

# Uses RAPIDS (CuDF) and GPU on Saturn Cloud to speed up embedding. Much larger subset (100k).
# input: arxiv-metadata-oai-snapshot.json
# output: arxiv_embeddings_100000.pkl

jupyter run multi-gpu-arxiv-embeddings.ipynb

# Uses RAPIDS and Dask (Dask CuDF) on Saturn Cloud to parallelize embedding creation. Much much larger subset (700k). Only output 300k to file.
# input: arxiv-metadata-oai-snapshot.json
# output: arxiv_embeddings_300000.pkl
```

### Benchmarks

```txt
arxiv-metadata-oai-snapshot.json ->
```

#### Generating Embeddings

| Model                    | Machine                      | Time   |
|-------------------------:|------------------------------|-------:|
|            `arxiv-embeddings.ipynb` | [Apple M1 Pro 8-core](https://www.apple.com/macbook-pro-14-and-16/specs/) | 17min |
|            `arxiv-embeddings.ipynb` | [Saturn Cloud T4-XLarge 4-cores](https://saturncloud.io/plans/hosted/) | 4min |
| `single-gpu-arxiv-embeddings.ipynb` | T4-XLarge 4-cores, `saturn-python-rapids` image | 30min |
|  `multi-gpu-arxiv-embeddings.ipynb` | Dask Cluster, 32 cores | ... |

#### Loading Index on Redis Cloud

| Model                    | Machine                      | Time   |
|-------------------------:|------------------------------|-------:|
|            `arxiv-embeddings.ipynb` | [Apple M1 Pro 8-core](https://www.apple.com/macbook-pro-14-and-16/specs/) | 17min |
