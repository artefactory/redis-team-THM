Title: Paper Classification Integration
Date: 2022-11-03 17:49
Modified: 2022-11-03 17:49
Category: Data Science
Tags: categories, huggingface, transformers
Slug: integrate-labels
Authors: (TODO)
Summary: (TODO)

_Day 10 - (TODO)_

# Model training pipeline

- Industrialization of the pipeline -> going from a notebook to scripts
    explain what we used from huggingface and put some links to tutorials and documentation
- storage of model -> local
    potential next step -> store the model elsewhere and develop a serving API 
- How to launch the pipeline
    Deduce from `retrain_model.sh`

# Inference pipeline

- Included inference pipeline into the encoding of the texts. 
    Rationale: use Redis to store the results --> avoids making prediction when using CLI (ensures smooth user experience)
    Challenge: encode the results in a string --> needed to create an encoding and decoding logic 
- For now, it uses a model stored locally that is the result of the model training pipeline
    In the future, we can imagine deploying the model somewhere and making an API call 

# Final result

Example of a redis object that gets updated to the database with the predicted soft labels