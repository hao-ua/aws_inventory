import sys
import os

class render:
    def __init__(self, output_folder, categories, pages):
        self.categories = categories
        self.items = {}
        self.Name = 'pureHTML'
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

    def printHeader(self):
        print '<html><head><title>AWS Inventory</title>'
        print '<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">'
        print '<link href="css/popup.css" rel="stylesheet" media="screen">'
        print '</head><body>'
        print '<script src="http://code.jquery.com/jquery.js"></script>'
        print '<script src="js/bootstrap.min.js"></script>'
        print '<br/> Links to <a href="index.csv">CSV</a>, <a href="inventory.xlsx">Excel</a><br/>'

    def printRow(self, rows, add_class, data, addFunction=None):
        print ''.join(['<tr class="', add_class, '">'])
        for val in rows:
            if add_class == 'header region':
                colspan = val[0]
            else:
                colspan = 1
            print ''.join(['<td colspan="', str(colspan), '">', str(data[val[1]]), '</td>'])
        if addFunction:
            addFunction(data)
        print '</tr>'

    def printCategoryItems(self, category, page):
        data = {}
        for key, val in map(lambda i,j:(i,j), self.HeaderKeys[page], self.HeaderRows[page]):
            data[key] = val
        self.printRow(map(lambda i,j: (i, j), self.HeaderRowWidths[page], self.HeaderKeys[page]), 'header', data)
        keyList = sorted(self.items[page][category].keys())
        for region_name in keyList:
            if len(self.items[page][category][region_name]) != 0:
                self.printRow([(str(len(self.HeaderKeys[page])),'region')], 'header region', {'region':region_name})
                itemList = sorted(self.items[page][category][region_name], key=lambda item: item['name'].upper())
                for item in itemList:
                    self.printRow(map(lambda i,j: (i,j), self.HeaderRowWidths[page], self.HeaderKeys[page]), 'trigger', item, self.printAddFunctions[page])

    def printFooter(self):
        print '</body></html>'

    def generatePage(self, page):
        for category in self.categories:
            print '<div class="tab', category, '">'
            print ''.join(['<div><h3 id="', category, '_', page, '">', category, '/', page, '</h3></div>'])
            print '<table>'
            self.printCategoryItems(category, page)
            print '</table>'
            print '</div>'

    def printContents(self, pages):
        print '<div class="contents"><div>Table of contents</div><ol>'
        for page in pages:
            for category in self.categories:
                print ''.join(['<li><a href="#', category, '_', page, '">', category, '/', page, '</a></li>'])
        print '</ol></div>'

    def render(self):
        self.backup = sys.stdout
        sys.stdout = open(''.join([self.output_folder, os.sep, 'index', '.html']), 'w')
        self.printHeader()
        self.printContents(self.pages)
        for page in self.pages:
            self.generatePage(page)
        self.printFooter()
        sys.stdout.close()
        sys.stdout = self.backup
