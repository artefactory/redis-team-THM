import logging
import pickle

import fire
import pandas as pd
from datasets import Dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          Trainer, TrainingArguments)
from transformers import logging as transformer_logging

from thm.config.settings import get_settings
from thm.utils_soft_labels import (apply_tokenenizer, clean_description,
                                   papers, prepare_labels)

config = get_settings()

transformer_logging.set_verbosity_error()
logging.getLogger().setLevel(logging.INFO)


def run(data_location: str, output_location: str):
    """
    This file generates soft labels for all the papers in the dataset.
    The data is expetected to be at: {config.data_location}/arxiv-metadata-oai-snapshot.json'
    The soft labels are saved at: {config.data_location}/soft_labels.pkl'

    You can increase the number of epochs to 2 or 3 to obtain better quality soft labels
    at the risk of overfitting the datatset.
    """

    logging.info('Reading data...')
    df = pd.DataFrame(papers(data_location))
    # df_with_paper_data = df.copy()

    logging.info('Cleaning data...')
    df['text'] = df.apply(lambda r: clean_description(r['title'] + ' ' + r['abstract']), axis=1).tolist()
    df = df[['text', 'categories']]

    # concatenate df and dummies (ooe_df will be used to inverse the preds and get category names)
    logging.info('Parsing and creating labels for categories...')
    df, ooe_df, num_classes = prepare_labels(df)

    # Create huggingface dataset object
    logging.info('Converting data to Dataset format')
    df_dataset = Dataset.from_pandas(df)
    # df_dataset = df_dataset.remove_columns('__index_level_0__')

    # Get and create tokenizer function
    logging.info('Loading tokenizer...')
    tokenizer = AutoTokenizer.from_pretrained(
        "prajjwal1/bert-tiny",
        problem_type="multi_label_classification",
        model_max_length=512
    )

    logging.info('Applying tokenizer...')
    df_dataset = apply_tokenenizer(df_dataset, tokenizer)

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
        output_dir=f'{output_location}/model_outputs',
        logging_steps=10000
    )
    trainer = Trainer(model=model, args=args, train_dataset=df_dataset, tokenizer=tokenizer)

    logging.info('Training model...')
    trainer.train()
    
    logging.info('Saving artifacts...')
    trainer.save_model()
    
    with open(f"{output_location}/categories.pkl", "wb") as cat_file:
        pickle.dump(ooe_df, cat_file)
        
if __name__ == "__main__":
    fire.Fire(run)
