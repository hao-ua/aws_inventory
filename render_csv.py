import sys
import os

class render:
    def __init__(self, output_folder, categories, pages):
        self.categories = categories
        self.items = {}
        self.Name = 'CSV'
        self.HeaderRows = {}
        self.HeaderRowWidths = {}
        self.HeaderKeys = {}
        self.printAddFunctions = {}
        self.pages = pages
        for page in self.pages:
            self.printAddFunctions[page] = None
        self.output_folder = output_folder

    def configPage(self, page, headerRows, headerRowWidths, headerKeys, data):
        self.HeaderRows[page] = headerRows
        self.HeaderRowWidths[page] = headerRowWidths
        self.HeaderKeys[page] = headerKeys
        self.items[page] = data

    def printRow(self, rows, add_class, data):
        items = [str(data[key]) for key in rows]
        print ','.join(items)

    def printCategoryItems(self, category, page):
        data = {}
        for key, val in map(lambda i,j:(i,j), self.HeaderKeys[page], self.HeaderRows[page]):
            data[key] = val
        self.printRow(self.HeaderKeys[page], 'header', data)
        keyList = sorted(self.items[page][category].keys())
        for region_name in keyList:
            print region_name
            if len(self.items[page][category][region_name]) != 0:
                self.printRow(['region'], 'header region', {'region':region_name})
                itemList = sorted(self.items[page][category][region_name], key=lambda item: item['name'].upper())
                for item in itemList:
                    self.printRow(self.HeaderKeys[page], 'trigger', item)

    def generatePage(self, page):
        for category in self.categories:
            print ''.join([page,'/',category])
            self.printCategoryItems(category, page)

    def render(self):
        self.backup = sys.stdout
        sys.stdout = open(''.join([self.output_folder, os.sep, 'index', '.csv']), 'w')
        for page in self.pages:
            self.generatePage(page)
        sys.stdout.close()
        sys.stdout = self.backup
