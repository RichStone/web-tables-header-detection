import os
import itertools
import json
import plotly
import re
from pprint import pprint
from definitions import PROJECT_ROOT_DIR
import requests


class WikiTablesReader:
    def __init__(self):
        #self.wiki_tables_json = os.environ['WIKI_TABLES_JSON_DUMP']
        self.wiki_tables_json = os.path.join(PROJECT_ROOT_DIR, '../data/tables.json')
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

    def query_string(self, key, search_value):
        """Search for a certain String value in the top level keys."""
        results = []
        for table in self.tables:
            if table[key]:
                value = table[key]
                if search_value in value:
                    results.append(table)
        return results

    def query_int(self, key, search_value):
        """Search for a certain int value in the top level keys."""
        results = []
        for table in self.tables:
            if table[key]:
                if search_value == table[key]:
                    results.append(table)
        return results

    def interestingHeader(self, ordinal):
        jsonTable = self.get(ordinal)
        print(jsonTable['pgId'])

        headerRows = jsonTable['tableHeaders']
        dataRows = jsonTable['tableData']

        #if len(headerRows) > 1:
        #    return True
        for row in dataRows + headerRows:
            for cell in row:
                html = cell['tdHtmlString']
                if '' in html:
                    print(html)
                    print(jsonTable['pgId'])
                    print(ordinal)
                    print(" ")
                    #return True
        return False

def getInterestingTables(wtr):
    interesting = 0
    notInteresting = 0

    for i in range(0, maxTable):
        if wtr.interestingHeader(i):
            interesting += 1
            #print("interesting")
        else:
            notInteresting += 1
            #print("not interesting")

    interestingPercent = 100 * interesting/maxTable
    print( " ")
    print("Percent of interesting Tables:")
    print(interestingPercent)
    
def getPureHtml(wtr):
    for i in range(0, 20):
        table = wtr.get(i)
        pgId = table['pgId']
        print(pgId)
        url = 'https://en.wikipedia.org/?curid=' + str(pgId)
        response = requests.get(url)
        splits = response.text.split('<table class="wikitable')
        if len(splits) != 2:
            print("there are the wrong number of tables on this page: " + str(len(splits) -1))
            continue
        htmlTable = splits[1].split('</table>')[0]
        if '<table' in htmlTable:
            print('there was a subtable we cannot deal with')
        else:
            print(htmlTable)

if __name__ == '__main__':
    wtr = WikiTablesReader()
    maxTable = 10000
    wtr.load_tables(maxTable)

    pprint(wtr.get(15))
    pprint(wtr.get(9824))
    
    
