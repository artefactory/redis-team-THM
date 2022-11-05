Title: Soft labels
Date: 2022-10-28 14:05
Modified: 2022-10-28 14:05
Category: Machine Learning
Tags: soft-labels, categories, bert
Slug: soft-labels
Authors: Tom Darmon
Summary: Creating soft labels for the users

_Day 6  - When we decided to quantify the categories of every article between 0 and 1._

## Help users find the balance between categories

Many research papers fall on the borderline between several categories. Let's suppose we are looking for a technical research paper in Computational Complexity using Machine Learning. We will probably find several papers with similar names that belong to both categories that interest us. But we are Machine Learning experts, we want the paper to talk mostly about Machine Learning.

How can we do this ?

## Soft labels

We decided to solve this issue by assigning a value between 0 and 1 for each category of every paper. It means that if you are using the `thm-cli` you will obtain a value that quantify each category.

Remember that we are a Machine Learning expert looking for research paper discussing Computational Complexity, we've found 2 interesting papers:

Paper 1

```
@article{yuan09,
    author = "Yuan Gao, Sheng Yu",
    title = "State Complexity Approximation",
    year = "2009",
    url = "https://arxiv.org/pdf/0907.5124.pdf",
    keywords = "..."
    cs.CC (90%), stat.ML (10%)
}
```

Paper 2

```
article{borja21,
    author = "Borja Rodr\'iguez-G\'alvez, Germ\'an Bassi, and Mikael Skoglund",
    title = "Tractable Inference for Complex Stochastic Processes",
    year = "2021",
    url = "https://arxiv.org/pdf/2005.05889.pdf",
    keywords = "..."
    cs.CC (30%), stat.ML (70%)
```


Both papers belong to the sames categories, but the first paper is only 10% about Machine Learning. We can directly have a look at the second paper, as it will focus on the subject we are interested in.


## How did we compute the score for the categories?


In order to obtain a fuzzy representation of categories, we decided to train `bert-tiny` on a multi label text classification problem. It was quite easy, as every article is already tagged with the categories. Our goal is not to correctly classify every category, we only want to model to quantify the degree of membership to each category.

The dataset is quite big, but the number of categories is relatively small, therefore we decided to train the model on only one epoch to avoid overfitting. One epoch gives our model a balance between correctly classifying the articles to the category they belong to but at the same the model didn't have time to learn the data by heart and produce score close to 1.

After computing the scores for each category offline, we only need to add the static data to our redis database and retrieve it to show it to you.

## Possible improvements

The main problem here is that if we train the model too long, we overfit the data and the predictions are equal to 1 for the real categories and 0 for the false categories (which is useless). But if we train the model too little we will obtain a model with mostly false predictions as he will not have time to converge.

Currently stopping the training after only one epoch is experimental, we can probably define a more rigorous protocol to select the best training parameters to compute the soft labels.