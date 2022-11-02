import json
from typing import List

with open("scripts/helpers/arxiv_taxonomy.json", "r") as taxonomy_file:
    taxonomy = json.load(taxonomy_file)

def parse_categories_from_redis(categories: str, sep: str=",") -> List[str]:
    categories_list = categories.split(sep)
    categories_labels = [taxonomy[category] for category in categories_list]
    
    return categories_labels
