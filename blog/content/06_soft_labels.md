Title: Soft labels
Date: 2022-10-28 14:05
Modified: 2022-10-28 14:05
Category: Machine Learning
Tags: data science, categories, huggingface, transformers
Slug: soft-labels
Authors: Tom Darmon
Summary: Creating soft labels for the users

_Day 6  - When we decided to quantify the categories of every article between 0 and 1._

## Help users find the balance between categories

Many research papers fall on the borderline between several categories. Let's suppose we are looking for a technical research paper in Computational Complexity using Machine Learning. We will probably find several papers with similar names that belong to both categories that interest us. But we are Machine Learning experts, we want the paper to talk mostly about Machine Learning.

How can we do this ?

## Soft labels

We decided to solve this issue by assigning a value between 0 and 1 for each category of every paper. It means that if you are using the `thm-cli` you will obtain a value that quantify each category.

Suppose you are a Machine Learning expert looking for research paper discussing Computational Complexity, we've found 2 interesting papers:

Paper 1

```
@article{alexa21
    author = "Alexandre d'Aspremont, Damien Scieur and Adrien Taylor",
    title = "Acceleration Methods",
    year = "2021",
    url = "https://arxiv.org/pdf/2101.09545.pdf",
}
```

Paper 2

```
@article{tanm20
    author = "Tan M. Nguyen, Richard G. Baraniuk, Andrea L. Bertozzi, Stanley J. Osher, Bao Wang",
    title = "MomentumRNN: Integrating Momentum into Recurrent Neural Networks",
    year = "2020",
    url = "https://arxiv.org/pdf/2006.06919.pdf",
}
```

Paper 1 is associated with the categories:
* Optimization and Control
* Machine Learning
* Numerical Analysis
* Numerical Analysis

While Paper 2 is categorised into:
* Optimization and Control
* Machine Learning
* Dynamical Systems

Both papers belong to the overlapping categories, so we want to be able to assign a weight to each category in order to be able to make a more informed decision.


## How did we compute the score for the categories?


In order to obtain a fuzzy representation of categories, we decided to use a pre-trained language model ([bert-tiny](https://huggingface.co/prajjwal1/bert-tiny)) on a multi label text classification problem. It was quite easy, as every article is already tagged with the categories.

The dataset is quite big, but the number of categories is relatively small, therefore we decided to train the model on only one epoch to avoid overfitting. One epoch gives our model a balance between correctly classifying the articles to the category they belong to but at the same the model didn't have time to learn the data by heart and produce score close to 1.

After computing the scores for each category offline, we only need to add the static data to our redis database and retrieve it to show it to the user.

## Possible improvements

The main problem here is that if we train the model too long, we risk overfitting the data and the predictions are equal to 1 for the real categories and 0 for the false categories (which is useless). But if we train the model too little we will obtain a model with mostly false predictions as it will not have time to converge.

Currently stopping the training after only one epoch is experimental, we can probably define a more rigorous protocol to select the best training parameters to compute the soft labels.

## Next Steps

In the next steps we will have to integrate this approach to our solution. This will involve creating separate training and serving pipelines for our model.