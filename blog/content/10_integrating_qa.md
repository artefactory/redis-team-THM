Title: Question Answering Integration
Date: 2022-11-03 15:28
Modified: 2022-11-03 15:28
Category: Data Science
Tags: question-answering, huggingface, transformers
Slug: integrate-answer
Authors: Henrique Brito
Summary: Integrating a question answering pipeline into our workflow

_Day 10 - Integrating the question answering approach into our workflow_

# Hugging Face pipeline

In the [last post]({filename}08_question_answering.md) we had decided to implement a Question Answering [pipeline](https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.QuestionAnsweringPipeline:~:text=passed%20as%20inputs.-,QuestionAnsweringPipeline,-class%20transformers.) from Huggingface to handle open-ended questions from users. After an experimentation phase performed on a notebook, we had to industrialize our code. Since the **question** input by the user has to be embedded with the **context** (in this case the papers titles and abstracts), we could not preemptively store the embeddings on Redis. This means that the embeddings have to be done in real-time when the user makes a question using the CLI. We implemented this logic in our [code]({filename}../../scripts/question_answering.py) using a function that we integrated in the CLI. 

# Leveraging Redis to speed up inference

One problem with this approach is that the embedding of large corpora can take a long time. If we want to look for the answer to a question among the entire arXiv dataset, we would need to encode all titles and abstracts every time the user submits a query. This would render the application impossible to use. In order to speed up the real-time inference we relied on RedisSearch to select a subset of priority papers that are most related to the users question. We make an API call to the endpoint `/vectorsearch/text/user` from our [backend]({filename}08_http_routes.md) and retrieve a list of papers that are most related to the question using the similarity between their embeddings. Once we have this list, we apply the pipeline to the corpora of all the texts combined and extract a response to the user's answer. 

# Results

We found that this feature showed interesting results for a first iteration. In many cases it could provide relevant answers to the user's questions:

```
Ask what is on your mind: what was stephen hawking most brilliant discovery?
--------------------------------------------------------------------------------
Answer: 'black holes have an entropy and consequently a finite temperature'
```

It manages to find names of domain-specific names of algorithms:

```
Ask what is on your mind: what is the best algorithm to multiply big matrix
--------------------------------------------------------------------------------
Answer: 'tSparse'
```

And even reply to open-ended questions: 

```
Ask what is on your mind: what are the challenges of climate change
--------------------------------------------------------------------------------
Answer: 'reducing inequalities and responsible consumption'
```

Even when the answer itself is not 100% pertinent, the paper where it came from can be a good reading suggestion

```
Ask what is on your mind: How to perform assortment optimization?
--------------------------------------------------------------------------------
Answer: 'using a computer algebra system'

This answer came from here:
A Computational Approach to Essential and Nonessential Objective Functions in Linear Multicriteria Optimization
by Agnieszka B. Malinowska, Delfim F. M. Torres
```

In other cases, the model seems to miss the point of the question:

```
Ask what is on your mind: What is machine learning?
--------------------------------------------------------------------------------
Answer: 'artificial intelligence'
```

```
Ask what is on your mind: how many colors in needed to color a map
--------------------------------------------------------------------------------
Answer: '6992 and 24'  
```

```
Ask what is on your mind: Can computer beat humans at the game of go?
--------------------------------------------------------------------------------
Answer: 'None of those agents succeeds in beating our agent' 
```

But most importantly, the results provided by this feature are seldom contained in the results of the vector search. This is encouraging as it increases the potential for serendipity of our global solution. 

# Future improvements

For this hackathon we used a pre-trained question answering model from Huggingface. The model we employed has been trained on a data from a large range of domains. This make so that scientific terms, which are not very common outside of the scientific community end up having a vector representation that is not nuanced enough to guarantee great performances. This problem could be mitigated by fine-tuning a question answering model with scientific questions. The biggest challenge in doing so is that these models require training sets with pre-annotated questions ans answer, which is very hard to achieve programmatically and would most likely have to done manually. 

Another problem with this approach is that, despite the optimizations brought by using Redis to choose priority papers, the inference time is still relatively long. The model currently takes about 45s to output answer. In the future, it would probably be best to migrate our technical stack to a framework such as [haystack](https://haystack.deepset.ai/overview/intro) instead of Huggingface. In addition to that, we could envisage deploying our model and making it available via an endpoint, instead of performing the calculations locally. This type of deployment come with significant security considerations, however, as the serving is usually done with the use of GPUs. 
