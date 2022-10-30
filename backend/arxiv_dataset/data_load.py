##### Imports
import string
import json
import re

##### Globals
YEAR_PATTERN = r"(19|20[0-9]{2})"

def parse_paper(paper: dict):
    paper = json.loads(paper)
    if paper['journal-ref']:
        years = [int(year) for year in re.findall(YEAR_PATTERN, paper['journal-ref'])]
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
        'abstract': paper['abstract']
    }
    
def clean_description(description: str):
    # TODO: review appropriate transformations
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