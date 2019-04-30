import os
from definitions import PROJECT_ROOT_DIR

wiki_tables_json = os.environ['WIKI_TABLES_JSON_DUMP']
output_dir = os.path.join(PROJECT_ROOT_DIR, 'data')

with open(wiki_tables_json) as file:
    for line in file:
        print(line)