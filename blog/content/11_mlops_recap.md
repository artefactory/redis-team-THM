Title: MLOps self-evaluation
Date: 2022-11-05 20:73
Modified: 2022-11-05 20:73
Category: MLOps
Tags: mlops, question-answering, soft-labels
Slug: 11_submission
Authors: Henrique Brito
Summary: Self-evaluation of the implementation of MLOps best practices

_Day 11 - Our self-evaluation of the MLOps maturity of this project._

# Introduction

Over the past two weeks we have proudly developed our [CLI tool]({filename}07_cli_tool.md) using RedisSearch. Even though we did not start from scratch, the time we had was very limited and we had to prioritize between brainstorming new ideas, learning new technologies, developing new features, and enforcing best practices. We are very aware that, in choosing our priorities, sometimes we had to opt for shortcuts that allowed us to keep going at a steady pace. Nonetheless, we believe that the work we have delivered is the best we could achieve in such a short time frame without decreasing the quality of the features we developed. In this article, we will therefore try to make an honest evaluation of the current MLOps maturity of the project and point out to possible future improvements. 

# ML Ops best practices

## Reproductibility

### Data

> Versioning data ensures that there is reproducibility in the process of creating models.

We were lucky to have a well curated and documented dataset to work with during this project. All the credits to the people who maintain this [data source](https://www.kaggle.com/datasets/Cornell-University/arxiv) open and free to use. 

### Code

> Versioning code allows to rollback to previous versions easily.

During the entire project we used git to version our code and github to collaborate between team members. We also worked with pull requests to develop new features and facilitate the reviewing process. 

### Model

> Versioning models allows to rollback to previous versions easily.

The model we trained for the [soft label generation]({filename}10_integrating_classification.md) has not been versioned. Given the simplicity of the modelling task, we achieved good performances from the first iteration. For this reason, we decided against prioritizing the versioning of the model. In the future, we can use tools such as MlFlow or AWS's SageMaker Model Registry to store our deployed models and their performances. 

## Scalability

### Data

> ML workflows need to be able to receive large volumes of data and different sources of data.

We developed a pipeline that automatically treats new data and stores it in the deployed Redis database. It takes less than 10 minutes to handle the data corresponding to one month and ensures that the data is accessible to the users. 

The pipeline employs two models: 
* a language model used to generate embeddings for each paper
* a text-classification model used to predict the category of the paper

For the first model, we use a pre-trained language model, so we did not have to deal with any considerations regarding training. To speed up our inference, we reduced the size of the generated vectors. While greatly improving the inference speeds, this can reduce the performance of our models. Nonetheless, we were satisfied with the recommendations the tool gave. 

For the second model, we created a training pipeline that can handle large volumes of data in an asynchronous fashion. Since this is detached from the model serving, we accepted longer execution times for this task. We prioritized using a compressed version of BERT to speed up the inference. This allowed us to keep inference times bellow 10s for a month of data. 

### Code

> Code needs to be parametrized to be able to scale efficiently when new business scopes need to leverage the work done.

We work with config files and static models to help us ensure code scalability. The first one ensure the code remains agnostic to hard-coded data such as model names and file paths, while the second one ensures we can use meaningful type hints and enforce static types. 

### Model

> Model training and inference need to ensure that processes run smoothly regardless of the data volumes

Here we can rely on the speed of Redis Search to guarantee the scalability of our solution. The serving time we observed while using this tool were reliably fast. 

For the beta feature of answering prompts input by the user, we currently rely on Huggingface's question answering pipelines. This is the biggest bottleneck we face in terms of inference times. In spite of the optimizations we did using Redis Search to narrow the selection of possible answers, the pipeline still takes about one minute to execute. In the future, we would like to explore more robust and scalable frameworks such as [haystack](https://haystack.deepset.ai/overview/intro).

## Monitoring

### Data

> Defining data tests with business knowledge ensures the quality of the data that enters into the ML pipeline

The use of static models ensures that the data we receive is correctly typed. Therefore, unexpected changes in the data should be caught by our current workflow. One thing we did not have the time to handle was checking the user inputs. For now we attempt to answer any kind of query a user makes. It would be great if, in the future, we enforce checks to these queries to ensure they are valid. 

### Code

> Developing unit tests / integration test make sure that all parts of the pipeline do what they are expected to do and that there is no regression when deploying new versions.

Given the limited amount of time we had at our disposal, we decided that developing new features was more relevant than writing robust tests.  

### Model

> Once they are deployed, machine learning models have to be monitored for model drift and production skew.

Once again the limited time-frame meant we could not tackle the monitoring of models. Nonetheless, we believe that constantly retraining the text-classification model with new data would be sufficient (on a temporary basis) to handle drift. 

## Automation

### Data

> Data need to be refreshed on a regular basis via an ETL pipeline

Since we are using a third-party dataset, we did not have to worry about updating the data. 

### Code

> Code is usually updated so it needs to be automatically tested and deployed via a CI/CD pipeline

For this project's CI, we set up GitHub actions to perform linting using `flake8`. In the future we can envisage incorporating our tests to this CI as well. Given the time-frame of the project, we judged that developing a CD was out of scope. 

### Model

> Machine Learning models need to be retrained on fresh data so it need to be automatically done via a CT pipeline

For now, model retraining has to be launched manually via our scripts. However, we can easily imagine using an orchestration tool such as Airflow to automatically do this. 