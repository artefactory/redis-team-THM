Title: Day 8 -Answering user's questions
Date: 2022-10-30 11:23
Modified: 2022-10-30 11:56
Category: Data Science
Tags: question-answering, huggingface, transformers
Slug: find-answer
Authors: Henrique Brito
Summary: Our data science approach to answer users' questions

_Day 8 - When we decided to explore a different way of researching information_

# Going back to fundamentals

Looking for information online has almost become a second nature to most people nowadays. After decades of being used to tools that can offer relevant answers to our queries, each one of us has developed techniques to get the best results. Most of the time, these techniques involve looking for keywords, filtering results, among others. During this project we wanted to propose a simpler way of looking for scientific information leveraging the data of arXiv. The core idea is to go back to the fundamentals of information retrieval: **answering a question**.

At the heart of every query there is a question that a user wants to answer. Differently from queries, questions are more natural to most people and reflect a precise need formulated by the user. Trying to answer them, while simple in a conversation, becomes remarkably difficult once we decide to do it programmatically. 

# The technical challenge

When trying to answer a question from an user, we need to deal with two problems simultaneously: understanding the question and finding the answer. The goal for this project is to map a scientific question to an answer extracted from the arXiv dataset. 

## Large language models

We decided to employ large pre-trained language models to help us achieve our goal. These models have been pre-trained on large corpora ranging a myriad of topics. Their large size and architecture have consolidated their place as state of the art models in almost all tasks of natural language processing. In this feature we will use models that have been trained for the Question Answering task. In general, these models expect a **context** and a **question** as inputs. They encode the information contained in both texts together and aim to extract the answer to the **question** using the information of the **context**. Because of this feature, they are called *extractive* question answering models and are, therefore, limited to the information contained in the **context**. 

# Next steps

In the next steps, we will be:
- Implementing a QA pipeline using Huggingface
- Using Redis to speedup the inference time
- Develop an interface to show results to the user

# Extra resources:

* More on question answering: [Hugginface](https://huggingface.co/tasks/question-answering), [Wikepedia](https://en.wikipedia.org/wiki/Question_answering)
