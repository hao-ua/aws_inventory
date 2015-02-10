import sys
import os
import openpyxl
from openpyxl.cell import get_column_letter
from openpyxl.styles import Alignment, Font, Style

class render:
    def __init__(self, output_folder, categories, pages):
        self.categories = categories
        self.items = {}
        self.Name = 'XLSX'
        self.HeaderRows = {}
        self.HeaderRowWidths = {}
        self.HeaderKeys = {}
        self.START_ROW = 1
        self.START_COLUMN = 1
        self.currentRow = self.START_ROW
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

    def printRow(self, page, rows, data, bold = False):
        items = [str(data[key]) for key in rows]
        if len(items) == 1 and len(items) != len(self.HeaderRows[page.title]):
            page.merge_cells(start_row=self.currentRow,start_column=self.START_COLUMN,end_row=self.currentRow,end_column=len(self.HeaderRows[page.title]))
        for index, val in enumerate(items, start=self.START_COLUMN):
            cell = page.cell(row = self.currentRow, column = index)
            cell.value = val
            if bold:
                cell.style = Style(font=Font(bold=bold),alignment=Alignment(horizontal='center',vertical='center',wrap_text=True))
            else:
                cell.style = Style(font=Font(bold=bold),alignment=Alignment(wrap_text=True))
        self.currentRow += 1

    def printCategoryItems(self, category, page):
        data = {}
        for key, val in map(lambda i,j:(i,j), self.HeaderKeys[page.title], self.HeaderRows[page.title]):
            data[key] = val
        self.printRow(page, self.HeaderKeys[page.title], data, True)
        keyList = sorted(self.items[page.title][category].keys())
        for region_name in keyList:
            if len(self.items[page.title][category][region_name]) != 0:
                self.printRow(page, ['region'], {'region':region_name.upper()}, True)
                itemList = sorted(self.items[page.title][category][region_name], key=lambda item: item['name'].upper())
                for item in itemList:
                    self.printRow(page, self.HeaderKeys[page.title], item)

    def generatePage(self, page):
        for category in self.categories:
            self.printRow(page, ['category'], {'category':category}, True)
            self.printCategoryItems(category, page)
            self.currentRow += 1

    def render(self):
        wb = openpyxl.Workbook()
        ws = wb.get_active_sheet()
        ws.title = self.pages[0]
        for page in self.pages[1:]:
            ws = wb.create_sheet()
            ws.title = page
        for page in self.pages:
            ws = wb.get_sheet_by_name(page)
            self.currentRow = self.START_ROW
            self.generatePage(ws)
            for i, val in enumerate(self.HeaderRowWidths[page]):
                ws.column_dimensions[get_column_letter(i+1)].width = int(val)*11
        wb.save(''.join([self.output_folder, os.sep, 'inventory.xlsx']))
