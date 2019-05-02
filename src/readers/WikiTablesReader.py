import os
import itertools
import json
from pprint import pprint
from definitions import PROJECT_ROOT_DIR


class WikiTablesReader:
    def __init__(self):
        self.wiki_tables_json = os.environ['WIKI_TABLES_JSON_DUMP']
        self.output_dir = os.path.join(PROJECT_ROOT_DIR, 'data')
        self.tables = []

    def load_tables(self, limit):
        with open(self.wiki_tables_json, 'r') as file:
            start_at = 0
            for line in itertools.islice(file, start_at, limit):
                table = json.loads(line)
                self.tables.append(table)

    def get(self, ordinal):
        return self.tables[ordinal]

    def query(self, key, search_value):
        """Search for a certain String value in the top level keys."""
        results = []
        for table in self.tables:
            if table[key]:
                value = table[key]
                if search_value in value:
                    results.append(table)
        return results


if __name__ == '__main__':
    wtr = WikiTablesReader()
    wtr.load_tables(500)
    pprint(wtr.get(55))
    pprint(wtr.query('_id', '10002087'))
