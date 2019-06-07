import os
import itertools
import json
import plotly
import re
from pprint import pprint
from definitions import PROJECT_ROOT_DIR
import requests


class WikiTablesReader:
    def __init__(self, fileName):
        #self.wiki_tables_json = os.environ['WIKI_TABLES_JSON_DUMP']
        self.wiki_tables_json = os.path.join(PROJECT_ROOT_DIR, fileName)
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

    def size(self):
        return len(self.tables)

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
    newTables = WikiTablesReader('../data/new/tables.json')
    oldTables = WikiTablesReader('../data/tables.json')
    
    maxTable = 5810
    newTables.load_tables(maxTable)
    oldTables.load_tables(maxTable)

    oldBold = 0
    newBold = 0

    oldItalic = 0
    newItalic = 0

    oldCentered = 0
    newCentered = 0

    oldCells = 0
    newCells = 0

    for i in range(0, maxTable):
        newTable = newTables.get(i)
        for cell in newTable['features']:
            newCells += 1
            if cell['isBold']: 
                newBold += 1
            if cell['isItalic']:
                newItalic += 1
            if cell['isCenterAligned']:
                newCentered += 1

        oldTable = oldTables.get(i)
        headerRows = oldTable['tableHeaders']
        dataRows = oldTable['tableData']
        for row in dataRows + headerRows:
            for cell in row:
                oldCells += 1
                html = cell['tdHtmlString']
                if re.search('((font-weight ?: ?bold)|(font ?: ?bold))', html):
                    oldBold += 1
                if re.search('(font-style ?: ?italic)', html):
                    oldItalic += 1
    print("Number of bold tags in old tables: ")
    print(oldBold)
    print("Number of bold tags in new tables: ")
    print(newBold)
    print("Number of bold tags in old tables: ")
    print(oldItalic)
    print("Number of italic tags in new tables: ")
    print(newItalic)
    print("number of cells in old tables:")
    print(oldCells)
    print("number of cells in new tables:")
    print(newCells)

    print("number of bold tags per cell in old tables:")
    print(oldBold/oldCells)
    print("number of bold tags per cell in new tables:")
    print(newBold/newCells)
    print("number of italic tags per cell in old tables:")
    print(oldItalic/oldCells)
    print("number of italic tags per cell in new tables:")
    print(newItalic/newCells)