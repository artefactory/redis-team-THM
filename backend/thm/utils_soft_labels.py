import json
import re
import string

import numpy as np

from thm.config.settings import get_settings

config = get_settings()


def clean_description(description: str):
    if not description:
        return ""
    # remove unicode characters
    description = description.encode('ascii', 'ignore').decode()

    # remove punctuation
    description = re.sub('[%s]' % re.escape(string.punctuation), ' ', description)

    # clean up the spacing
    description = re.sub('\s{2,}', " ", description)

    # remove urls
    #description = re.sub("https*\S+", " ", description)

    # remove newlines
    description = description.replace("\n", " ")

    # remove all numbers
    #description = re.sub('\w*\d+\w*', '', description)

    # split on capitalized words
    description = " ".join(re.split('(?=[A-Z])', description))

    # clean up the spacing again
    description = re.sub('\s{2,}', " ", description)

    # make all words lowercase
    description = description.lower()

    return description

# Generator functions that iterate through the file and process/load papers


def process(paper: dict):
    paper = json.loads(paper)
    if paper['journal-ref']:
        # Attempt to parse the date using Regex: this could be improved
        years = [int(year) for year in re.findall(config.year_pattern, paper['journal-ref'])]
        years = [year for year in years if (year <= 2022 and year >= 1991)]
        year = min(years) if years else None
    else:
        year = None
    return {
        'id': paper['id'],
        'title': paper['title'],
        'year': year,
        'authors': paper['authors'],
        'categories': ','.join(paper['categories'].split(' ')),
        'abstract': paper['abstract'], }


def papers():
    with open(f'{config.data_location}/arxiv-metadata-oai-snapshot.json', 'r') as f:
        for paper in f:
            paper = process(paper)
            # Yield only papers that have a year I could process
            if paper['year']:
                yield paper


def get_best_args_and_score(row):
    # get 3 best predictions
    best_args = np.argpartition(row, -3)[-3:]
    best_score = row[best_args]
    return best_args, best_score


def get_category_names(args, ooe_df):
    # get category names from args
    return ooe_df.columns[args[0].astype(int).tolist()]
