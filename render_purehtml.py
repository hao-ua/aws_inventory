import sys
import os


class Render(object):
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

    def config_page(self, page, header_rows, header_row_widths, header_keys, data):
        self.HeaderRows[page] = header_rows
        self.HeaderRowWidths[page] = header_row_widths
        self.HeaderKeys[page] = header_keys
        self.items[page] = data

    @staticmethod
    def print_header():
        print '<html><head><title>AWS Inventory</title>'
        print '<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">'
        print '<link href="css/popup.css" rel="stylesheet" media="screen">'
        print '</head><body>'
        print '<script src="http://code.jquery.com/jquery.js"></script>'
        print '<script src="js/bootstrap.min.js"></script>'
        print '<br/> Links to <a href="index.csv">CSV</a>, <a href="inventory.xlsx">Excel</a><br/>'

    @staticmethod
    def print_row(rows, add_class, data, add_function=None):
        print ''.join(['<tr class="', add_class, '">'])
        for val in rows:
            if add_class == 'header region':
                colspan = val[0]
            else:
                colspan = 1

            print ''.join(['<td colspan="', str(colspan), '">', str(data[val[1]]), '</td>'])
        if add_function:
            add_function(data)

        print '</tr>'

    def print_category_items(self, category, page):
        data = dict()
        for key, val in map(lambda i, j: (i, j), self.HeaderKeys[page], self.HeaderRows[page]):
            data[key] = val

        self.print_row(map(lambda i, j: (i, j), self.HeaderRowWidths[page], self.HeaderKeys[page]), 'header', data)
        key_list = sorted(self.items[page][category].keys())
        for region_name in key_list:
            if len(self.items[page][category][region_name]) != 0:
                self.print_row([(str(len(self.HeaderKeys[page])), 'region')], 'header region', {'region': region_name})
                item_list = sorted(self.items[page][category][region_name], key=lambda x: x['name'].upper())
                for item in item_list:
                    self.print_row(map(lambda i, j: (i, j), self.HeaderRowWidths[page], self.HeaderKeys[page]),
                                   'trigger', item, self.printAddFunctions[page])

    @staticmethod
    def print_footer():
        print '</body></html>'

    def generate_page(self, page):
        for category in self.categories:
            print '<div class="tab', category, '">'
            print ''.join(['<div><h3 id="', category, '_', page, '">', category, '/', page, '</h3></div>'])
            print '<table>'
            self.print_category_items(category, page)
            print '</table>'
            print '</div>'

    def print_contents(self, pages):
        print '<div class="contents"><div>Table of contents</div><ol>'
        for page in pages:
            for category in self.categories:
                print ''.join(['<li><a href="#', category, '_', page, '">', category, '/', page, '</a></li>'])

        print '</ol></div>'

    def render(self):
        backup = sys.stdout
        sys.stdout = open(''.join([self.output_folder, os.sep, 'index', '.html']), 'w')
        self.print_header()
        self.print_contents(self.pages)
        for page in self.pages:
            self.generate_page(page)

        self.print_footer()
        sys.stdout.close()
        sys.stdout = backup
