
<div align="center">
    <img src="https://github.com/RedisVentures/redis-arXiv-search/blob/main/backend/vecsim_app/data/redis-logo.png?raw=true" height="30" />
    <img src="https://www.cbnews.fr/sites/cbnews.fr/files/logo-societe/2019-05/Logo%20Artefact.png" height="20" />
</div>

## Contents

This demo showcases the vector search similarity (VSS) capability within Redis Stack and Redis Enterprise.

Through the RediSearch module, vector types and indexes can be added to Redis. This turns Redis into
a highly performant vector database which can be used for all types of applications.

![Screen Shot 2022-09-20 at 12 20 16 PM](https://user-images.githubusercontent.com/13009163/191346916-4b8f648f-7552-4910-ad4e-9cc117230f00.png)

## Documentation

- [Basic Demo](https://docsearch.redisventures.com) | [GitHub](https://github.com/RedisVentures/redis-arXiv-search)
- [Redis Vector Similarity Search](https://redis.io/docs/stack/search/reference/vectors)
- [Cornell University - arXiv dataset](https://www.kaggle.com/Cornell-University/arxiv), `arxiv-metadata-oai-snapshot.json` file is used

## History

- Forked from [`RedisVentures/redis-arXiv-search`](https://github.com/RedisVentures/redis-arXiv-search)
- Used Tyler Hutcherson's latest changes: [PR 3](https://github.com/RedisVentures/redis-arXiv-search/pull/3), [PR 9](https://github.com/RedisVentures/redis-arXiv-search/pull/9)

## Setup

```sh
brew install yarn redis
```

## Application

This app was built as a Single Page Application (SPA) with the following components:

- **[Redis Stack](https://redis.io/docs/stack/)**: Vector database + JSON storage
- **[FastAPI](https://fastapi.tiangolo.com/)** (Python 3.8)
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** for schema and validation
- **[React](https://reactjs.org/)** (with Typescript)
- **[Redis OM](https://redis.io/docs/stack/get-started/tutorials/stack-python/)** for ORM
- **[Docker Compose](https://docs.docker.com/compose/)** for development
- **[MaterialUI](https://material-ui.com/)** for some UI elements/components
- **[React-Bootstrap](https://react-bootstrap.github.io/)** for some UI elements
- **[Huggingface Tokenizers + Models](https://huggingface.co/sentence-transformers)** for vector embedding creation

Some inspiration was taken from this [Cookiecutter project](https://github.com/Buuntu/fastapi-react)
and turned into a SPA application instead of a separate front-end server approach.

## Running Locally

> Before running locally - you should download the data and run through the `arXivPrepSubset.ipynb` notebook to generate some sample embeddings.

Setup python environment

- If you use conda, take advantage of the Makefile included here: `make env`
- Otherwise, setup your virtual env however and install python deps in `requirements.txt`

To launch app, run the following

- `docker compose up` in same directory as `docker-compose.yml`
- Navigate to `http://localhost:8888` in a browser

### Building the containers

```sh
docker compose up

# To force a new build
docker compose up --build
```

### Frontend Application

```sh
cd frontend
yarn install --no-optional
yarn start
open http://localhost:3000
```

### Troubleshooting

#### Issues building the container

- Sometimes it works if you try again. Or maybe you need to clear out some Docker cache. Run `docker system prune`, restart Docker Desktop, and try again.
- The generated `node_modules` folder (under `gui/` when running the app outside of Docker) can mess things up when building docker images. Delete that folder (if present) and try rebuilding again.
