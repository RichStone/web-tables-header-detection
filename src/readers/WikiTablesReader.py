import os
import itertools
import json
import plotly
from pprint import pprint
from definitions import PROJECT_ROOT_DIR


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

    def displayTable(self, ordinal):
        jsonTable = self.get(ordinal)
        cellColors = []
        textTable = []

        headerRows = jsonTable['tableHeaders']
        dataRows = jsonTable['tableData']
        for row in (headerRows + dataRows):
            rowColors = []
            textRow = []
            for cell in row:
                text = cell['text']
                if "Error: " in text:
                    text = "Error: ..."
                textRow.append(text)
                html = cell['tdHtmlString']
                if "<th " not in html:
                    rowColors.append('#EDFAFF')
                else:
                    rowColors.append('#a1c3d1')
            cellColors.append(rowColors)
            textTable.append(textRow)
        
        plotTable = plotly.graph_objs.Table(
            cells=dict(values=textTable,
                line = dict(color='#7D7F80'),
                fill = dict(color=cellColors))
        )
        data = [plotTable] 
        plotly.plotly.iplot(data, filename = 'header_highlighted')
        print("plotted table")

if __name__ == '__main__':
    wtr = WikiTablesReader()
    wtr.load_tables(60)
    pprint(wtr.get(10))
    pprint(wtr.query_int('numHeaderRows', 5))
    wtr.displayTable(10)
