from enum import Enum
import json
import re 
from dateutil.parser import parse

class Alignment(Enum):
    LEFT = 0
    CENTERED = 1
    RIGHT = 2

class NumberFormat(Enum):
    INTEGER = 0
    DECIMAL = 1
    EXPONENTIAL = 2
    HEXADECIMAL = 3
    BINARY = 4
    # add dateFormats?

class CellFeatures:
    def __init__(self, cell):
        html = str(cell['tdHtmlString'])
        text = cell['text']
        self.isMerged = re.search('((colspan ?= ?"(?!1"))|(rowspan ?= ?"(?!1")))', html)
        # self.alginment
        # TODO: look at text-align and vertical-align standard values
        # in table 15 (pgId 1000072, table 15) there is no alignment info even though there is on inspect element
        self.isBold = html.find("<th") == 0 or re.search('((font-weight ?: ?bold)|(font ?: ?bold))', html)
        # table 10275067 (9824) has bold tag in html, but not in crawled data
        self.isItalic = re.search('(font-style ?: ?italic)', html)
        self.isColored = html.find("<th")
        # self.font
        # self.format number format? how to determine?
        self.isEmpty = len(text) == 0
        self.isText = not cell['isNumeric']
        self.isNumeric = cell['isNumeric']
        try: 
            parse(text)
            self.isDate = True
        except ValueError:
            self.isDate = False
        
        # TODO: determine one standard deviation from mean cell text in a sample of data tables
        # self.isShortText
        # self.isLongText
        self.isTotal = 'total' in cell['text'].lower
