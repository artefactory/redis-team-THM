import pandas as pd 
import numpy as np
from datasets import Dataset
import torch
from transformers import logging as transformer_logging
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from transformers import Trainer, TrainingArguments
import logging
import pickle

from utils_soft_labels import clean_description, process, papers, get_best_args_and_score, get_category_names
from config import DATA_LOCATION

transformer_logging.set_verbosity_error()
logging.getLogger().setLevel(logging.INFO)

def main():
    logging.info('Reading data...')
    df = pd.DataFrame(papers())
    df = df.sample(100)
    df_with_paper_data = df.copy()

    logging.info('Cleaning data...')
    df['text'] = df.apply(lambda r: clean_description(r['title'] + ' ' + r['abstract']), axis=1).tolist()
    df = df[['text', 'categories']]

    # concatenate df and dummies (ooe_df will be used to inverse the preds and get category names)
    logging.info('Parsing and creating labels for categories...')
    ooe_df = df['categories'].str.get_dummies(sep=',')
    num_classes = ooe_df.shape[1]
    category_cols = ooe_df.columns.tolist()
    parse_labels = lambda x : [x[c] for c in category_cols]

    # parse the labels
    df['labels'] = ooe_df.apply(parse_labels, axis=1)
    df = df[['text', 'labels']]

    # Create huggingface dataset object
    logging.info('Converting data to Dataset format')
    df_dataset = Dataset.from_pandas(df)
    df_dataset = df_dataset.remove_columns('__index_level_0__')

    # Get and create tokenizer function
    logging.info('Loading tokenizer...')
    tokenizer = AutoTokenizer.from_pretrained(
        "prajjwal1/bert-tiny",
        problem_type="multi_label_classification",
        model_max_length=512
        )
    def tokenize_and_encode(examples):
        return tokenizer(examples["text"], truncation=True)
    cols = df_dataset.column_names
    cols.remove('labels')

    logging.info('Applying tokenizer...')
    df_dataset = df_dataset.map(tokenize_and_encode, batched=True, remove_columns=cols)
    df_dataset.set_format("torch")
    df_dataset = (df_dataset
            .map(lambda x : {"float_labels": x["labels"].to(torch.float)}, remove_columns=["labels", "token_type_ids"])
            .rename_column("float_labels", "labels"))

    # Modeling 
    logging.info('Loading model...')
    model = AutoModelForSequenceClassification.from_pretrained(
    "prajjwal1/bert-tiny",
    num_labels=num_classes,
    problem_type="multi_label_classification"
    )

    args = TrainingArguments(
    save_strategy="epoch",
    num_train_epochs=1,
    output_dir = f'{DATA_LOCATION}/model_outputs',
    logging_steps = 10000
)
    trainer = Trainer(model=model, args=args, train_dataset=df_dataset, tokenizer=tokenizer)

    logging.info('Training model...')
    trainer.train()

    logging.info('Computing predictions...')
    preds = trainer.predict(df_dataset)
    preds = preds.predictions
    preds = torch.nn.functional.softmax(torch.tensor(preds))

    # Add soft labels back into df with papers data
    logging.info('Preparing final output format...')
    best_args_score_vec = np.apply_along_axis(get_best_args_and_score, 1, preds)
    categories_vec = np.apply_along_axis(get_category_names, 1, best_args_score_vec, ooe_df)
    best_score =  best_args_score_vec[:,1]
    soft_tags = {'category' : categories_vec.tolist(), 'score' : np.around(best_score, 2).tolist()}
    df_with_paper_data['category_predicted'] = soft_tags['category']
    df_with_paper_data['category_predicted'] = df_with_paper_data['category_predicted'].str.join(',')
    df_with_paper_data['category_score'] = soft_tags['score']

    # Dump these to file with pickle or write them to Redis
    logging.info(f'Saving final output to {DATA_LOCATION}...')
    with open(f'{DATA_LOCATION}/papers_with_soft_labels.pkl', 'wb') as f:
        pickle.dump(df_with_paper_data, f)

if __name__ == "__main__":
    main()