Title: The Redis Hackathon
Date: 2022-10-15 01:15
Modified: 2022-10-15 1:15
Category: RediSearch
Tags: mlops, hackathon
Slug: mlops-methodology
Authors: Michel Hua
Summary: The Redis Hackathon

_Day 1 - This article is the first of a series of posts we will do during the [Redis Venture hackathon](https://hackathon.redisventures.com). The goal is to keep a journal of our work._

# What is MLOps?

MLOps is a term to describe general software engineering principles applied to the problems of serving machine learning models in production.

# Code Best Practices

## Building Python

Using GitHub Actions, we [checked our code](https://github.com/artefactory/redis-team-THM/blob/main/.github/workflows/ci-python.yml) against the `main` branch of the repo, ensuring not only style but also variables linking remain safe during development.

We used [`flake8`](https://github.com/PyCQA/flake8) for basic linting and [`black`](https://github.com/psf/black) for code formatting.

Static analysis is essential in Python because the language uses duck typing and this can cause issues during runtime, problems that a compiler would have caught.

Improving readability, ensuring formatting and style, is essential to the team of developers.

# Model Deployment

## Ways to deploy a model

In a Python Machine Learning project, prototypes usually are written using Jupyter notebooks, such as the ones in the [`redis-arXiv-search/data`](https://github.com/RedisVentures/redis-arXiv-search/tree/main/data) repository.

The first step to make it more professional, is to turn it to a pipeline. Pipelines usually are decomposed in steps which are responsible for handling one input file and another file as output.

The first step is to write a Python module component that enables us to produce a model, under certain conditions, and to be able to rerun it in a flexible way.

In Python, there are open source tools which help you in that process. For example, [`mlflow/mlflow`](https://github.com/mlflow/mlflow) to deal with the lifecycle of training your models, measuring their performance and archiving models. In other situations, you might also want to run advanced pipelines with [`apache/airflow`](https://github.com/apache/airflow) which can take care of different steps such as data fetching, pre-processing and handling executions in different context with DAGs.

After scheduling the execution of this training component and storing the models, we usually need to serve the models to the end user.

Serving a model means performing predictions or getting the results of large numerical computations. Today, models are usually served through web servers and communicate with other applications through HTTP requests.

In Python, you would serve a REST API with the [`tiangolo/fastapi`](https://github.com/tiangolo/fastapi) framework, use a database such as [`redis/redis`](https://github.com/redis/redis) to store your predictions. This is usually the case in systems like search engines or recommendation systems.

REST APIs allows clients to ask for a service in real time and get an answer quickly. Most website modern websites are designed this way. You can think of transportation information systems where the information has to be updated every minute.

We will see later how to leverage these concepts in the Redis Hackathon.

# The Redis Hackathon

The [Vector Search Engineering Lab](https://hackathon.redisventures.com) hackathon is happening from October 24 to November 4, we have decided to participate with 4 engineers from Artefact. It is a hackathon centered of Vector Search using Redis technologies and the arXiv papers dataset.

The goal is to demonstrate through a small project how easy and powerful the following techniques are applicable to a modern web application problem:

- [vector similarity search](https://en.m.wikipedia.org/wiki/Similarity_search)
- [Natural Language Processing](https://en.m.wikipedia.org/wiki/Natural_language_processing)
- [Text Mining](https://en.m.wikipedia.org/wiki/Text_mining)
- [Knowledge Graphs](https://en.m.wikipedia.org/wiki/Knowledge_graph)
- [Document Retrieval](https://en.m.wikipedia.org/wiki/Document_retrieval)
- [Topic Identification](https://en.m.wikipedia.org/wiki/Topic_model)
- [Question & Answering](https://en.m.wikipedia.org/wiki/Question_answering)
- [Recommendation Systems](https://en.m.wikipedia.org/wiki/Recommender_system)
- [Data Visualization](https://en.m.wikipedia.org/wiki/Data_and_information_visualization)

Using the right MLOps tools and technologies, we will build interesting experiences for all the users who want to search for scientific papers!

# References

- [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp/)
- [Vector Search Engineering Lab](https://hackathon.redisventures.com)