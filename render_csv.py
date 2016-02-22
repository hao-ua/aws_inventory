import sys
import os


class Render(object):
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

    def config_page(self, page, header_rows, header_row_widths, header_keys, data):
        self.HeaderRows[page] = header_rows
        self.HeaderRowWidths[page] = header_row_widths
        self.HeaderKeys[page] = header_keys
        self.items[page] = data

    @staticmethod
    def print_row(rows, data):
        items = [str(data[key]) for key in rows]
        print ','.join(items)

    def print_category_items(self, category, page):
        data = {}
        for key, val in map(lambda i, j: (i, j), self.HeaderKeys[page], self.HeaderRows[page]):
            data[key] = val

        self.print_row(self.HeaderKeys[page], data)
        key_list = sorted(self.items[page][category].keys())
        for region_name in key_list:
            print region_name
            if len(self.items[page][category][region_name]) != 0:
                self.print_row(['region'], {'region': region_name})
                item_list = sorted(self.items[page][category][region_name], key=lambda x: x['name'].upper())
                for item in item_list:
                    self.print_row(self.HeaderKeys[page], item)

    def generate_page(self, page):
        for category in self.categories:
            print ''.join([page, '/', category])
            self.print_category_items(category, page)

    def render(self):
        backup = sys.stdout
        sys.stdout = open(''.join([self.output_folder, os.sep, 'index', '.csv']), 'w')
        for page in self.pages:
            self.generate_page(page)

        sys.stdout.close()
        sys.stdout = backup
