Title: Services Endpoints
Date: 2022-10-30 12:05
Modified: 2022-10-30 12:05
Category: MLOps
Tags: hackathon
Slug: services
Authors: Corentin Roineau
Summary: Services Endpoints

_Day 8 - When we studied the routes of our API_

# Endpoints of the project

In the project, we have two main *services* with which HTTP clients can interact with. When users make a requests, the backend connects to the Redis database and answers to requests.

You can find the Swagger documentation here,

<div align="center">
    <a href="https://thm-cli.community.saturnenterprise.io/api/docs">https://thm-cli.community.saturnenterprise.io/api/docs</a>
</div>

## Route processing HTTP request

<div align="center">
    <img src="https://miro.medium.com/max/1304/1*qvwLjnj2ExA707IZyUXLLw.png" width=300>
</div>

# Recap of the different routes

Don't forget that you can call each API with your application to get the data from our databases.

| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| `/vectorsearch/text` | POST | Retrieve a similar list of papers to a paper_id | `{"user_text": "string", "categories": ["physics.space-ph"], "years": ["1969"], "number_of_results": 5,"search_type": "KNN"}` | `{"papers": [{"id": "123", "title": "title", "abstract": "abstract"}, ...]}` |
| `/vectorsearch/text/user` | POST | Retrieve a list of papers matching user's text input | `{"user_text": "string", "categories": ["physics.space-ph"], "years": ["1969"], "number_of_results": 5,"search_type": "KNN"}` | `{"papers": [{"id": "123", "title": "title", "abstract": "abstract"}, ...]}` |

## `/vectorsearch/text`

```
% curl 'https://thm-cli.community.saturnenterprise.io/api/v1/paper/vectorsearch/text' \
  -H 'Content-Type: application/json' \
  --data-raw '{"paper_id":"0804.1457","search_type":"KNN","number_of_results":15,"years":["2022","2020"],"categories":["math-ph"]}'

{"total":58,"papers":[{"predicted_categories":"cond-mat.stat-mech(0.7070)|cond-mat.dis-nn(0.2019)|cond-mat.str-el(0.1755)","categories":"math-ph|cond-mat.str-el|math.MP","paper_id":"2112.07180","authors":"Pei Sun, Jintao Yang, Yi Qiao, Junpeng Cao and Wen-Li Yang","title":"Scattering matrix of elementary excitations in the antiperiodic XXZ spin\n  chain with \\eta=i\\pi/3","abstract":"  We study the thermodynamic limit of the antiperiodic XXZ spin chain with the\nanisotropic parameter $\\eta=\\frac{\\pi i}{3}$. We parameterize eigenvalues of\nthe transfer matrix by their zero points instead of Bethe roots. We obtain\npatterns of the distribution of zero points. Based on them, we calculate the\nground state energy and the elementary excitations in the thermodynamic limit.\nWe also obtain the two-body scattering matrix of elementary excitations. Two\ntypes of elementary excitations and three types of scattering processes are\ndiscussed in detailed.\n","year":"2022","similarity_score":0.482848227024}, ...]}
```

## `/vectorsearch/text/user`

```sh
% curl 'https://thm-cli.community.saturnenterprise.io/api/v1/paper/vectorsearch/text/user' \
  -H 'Content-Type: application/json' \
  --data-raw '{"user_text":"people review","search_type":"KNN","number_of_results":15,"years":[],"categories":[]}'

{"total":59114,"papers":[{"predicted_categories":"cs.LG(0.1989)|cs.AI(0.1547)|cs.CL(0.1235)","categories":"cs.DL|cs.AI|cs.DS","paper_id":"cs/0605112","authors":"Marko A. Rodriguez, Johan Bollen","year":"2008","title":"An Algorithm to Determine Peer-Reviewers","abstract":"  The peer-review process is the most widely accepted certification mechanism\nfor officially accepting the written results of researchers within the\nscientific community. An essential component of peer-review is the\nidentification of competent referees to review a submitted manuscript. This\narticle presents an algorithm to automatically determine the most appropriate\nreviewers for a manuscript by way of a co-authorship network data structure and\na relative-rank particle-swarm algorithm. This approach is novel in that it is\nnot limited to a pre-selected set of referees, is computationally efficient,\nrequires no human-intervention, and, in some instances, can automatically\nidentify conflict of interest situations. A useful application of this\nalgorithm would be to open commentary peer-review systems because it provides a\nweighting for each referee with respects to their expertise in the domain of a\nmanuscript. The algorithm is validated using referee bid data from the 2005\nJoint Conference on Digital Libraries.\n","similarity_score":0.451238274574}, ...]}
```
