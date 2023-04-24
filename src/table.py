'''
Describes a data table for seeing all transactions
'''

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

from config import *

class BarChart:
    def __init__(self, root, labels, data, row, col, xaxis, yaxis, title=""):
        self.title = title
        self.labels = labels
        self.data = data
        self.fig, self.ax = plt.subplots(figsize=(5, 2.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.xaxis_title = xaxis
        self.yaxis_title = yaxis
        self.drawChart()
        self.canvas.get_tk_widget().grid(row=row, column=col)
        plt.xticks(rotation=45)
        plt.tight_layout()

    def drawChart(self):
        # self.ax.clear()
        self.ax.bar(self.labels, self.data)
        self.ax.set_xlabel(self.xaxis_title)
        self.ax.set_ylabel(self.yaxis_title)
        self.ax.set_title(self.title)

class PieChart:
    def __init__(self, root, labels, data, row, col, title=""):
        self.title = title
        self.labels = labels
        self.data = data
        self.percentages = self.getPercentages()
        self.labels_wperc = self.getPercentLabels()
        plt.rcParams['font.size'] = 8
        self.fig, self.ax = plt.subplots(figsize=(5, 2.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)

        self.drawChart()
        self.canvas.get_tk_widget().grid(row=row, column=col)

    def getPercentages(self):
        total = 0
        percs = []
        for d in self.data:
            total += d
        for d in self.data:
            percs.append((d/total) *100)
        return percs

    def getPercentLabels(self):
        labels = []
        for i,l in enumerate(self.labels):
            labels.append(self.labels[i] + ' ('+str(round(self.percentages[i], 2))+'%)')
        return labels
    
    def drawChart(self):
        # self.ax.clear()
        wedges, labels, autotexts = self.ax.pie(self.data, labels=self.labels, autopct="%1.1f%%", textprops={'fontsize': 8}, startangle=90, pctdistance=0.8, labeldistance=1.2)
        self.ax.set_position((-0.05, 0.1, 0.8, 0.8))     # left, bottom, width, height
        self.ax.legend(self.labels, loc='center', bbox_to_anchor=(1.75, 0.5))
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
            try:
                if len(r[index]) > length:
                    length = len(r[index])
            except TypeError:
                length = 10
        return length