# Team THM Submission

<div align="center">
    <img src="https://github.com/RedisVentures/redis-arXiv-search/blob/main/backend/vecsim_app/data/redis-logo.png?raw=true" height="25" /> <br />
    <img src="https://www.cbnews.fr/sites/cbnews.fr/files/logo-societe/2019-05/Logo%20Artefact.png" height="20" /><br />
    October - November 2022
</div>
<br />

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
                        writes index
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
+--------+----------+
|                   |
|  React            |
|                   |
+-------------------+
            browser use app from here
```

</details>

## Running The Application

### Running With Docker

```sh
docker compose up
open http://localhost:8888

# To force a new build
docker compose up --build

# To clear Docker cache
docker system prune
```

### Backend Application Only

```sh
cd backend/
```

### Frontend Application Only

```sh
cd frontend/
yarn install --no-optional
yarn start
open http://localhost:3000
```

### Machine Learning Model

First, download the data and run the `arXivPrepSubset.ipynb` notebook to generate some embeddings.

```sh
cd datascience/
# ...
```
