'''
Describes a data table for seeing all transactions
'''

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from config import *

class PieChart:
    def __init__(self, root, labels, data, title=""):
        self.title = title
        self.labels = labels
        self.data = data
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=1, column=0)

        self.drawChart()
    
    def drawChart(self):
        self.ax.clear()
        self.ax.pie(self.data, labels=self.labels, autopct="%1.1f%%", startangle=90)
        self.ax.axis("equal")
        self.ax.set_title(self.title)
        self.canvas.draw()


class DataTable:
    def __init__(self, window, headers, data, st_row, st_col):
        self.headers = headers
        self.window = window
        self.header_font = SMALL_FONT
        self.cell_font = SMALL_FONT
        self.st_row = st_row
        self.st_col = st_col
        self.table = ttk.Treeview(self.window, selectmode='browse', height=20)
        self.table.grid(row=self.st_row, column=self.st_col)
        self.data = data

        if data:
            self.createHeaders()
            self.addData()

    def createHeaders(self):
        self.table["columns"] = tuple(self.headers)
        self.table["show"] = 'headings'
        self.table.heading("#0", text="ID")
        for i,h in enumerate(self.headers):
            self.table.heading(h, text=h)
            self.table.column(i, width=10*self.getHeaderSize(i), anchor='c')

    def addData(self):
        for r in self.data:
            self.table.insert("", 'end', values=(r))

    def getHeaderSize(self, index):
        length = 0
        for r in self.data:
            if len(r[index]) > length:
                length = len(r[index])
        return length