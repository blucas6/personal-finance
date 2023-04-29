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
    def __init__(self, root, labels, data, row, col, xaxis, yaxis, size, colors="", columnspan=0, title=""):
        self.title = title
        self.fig, self.ax = plt.subplots(figsize=(size[0], size[1]))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.xaxis_title = xaxis
        self.yaxis_title = yaxis
        self.drawChart(labels, data, colors=colors)
        self.widget = self.canvas.get_tk_widget()
        if columnspan > 0:
            self.widget.grid(row=row, column=col, columnspan=columnspan)
        else:
            self.widget.grid(row=row, column=col)
    
    def drawChart(self, headers, data, colors=""):
        self.ax.clear()
        if colors:
            self.ax.bar(headers, data, color=colors)
        else:
            self.ax.bar(headers, data)
        self.ax.set_xlabel(self.xaxis_title)
        self.ax.set_ylabel(self.yaxis_title)
        self.ax.set_title(self.title)
        for tick in self.ax.get_xticklabels():
            tick.set_rotation(75)
        plt.tight_layout()
        self.canvas.draw()

class PieChart:
    def __init__(self, root, labels, data, row, col, title="", threshold_percent=2):
        self.title = title
        self.labels = labels
        self.data = data
        self.threshold = threshold_percent
        self.percentages = self.getPercentages()
        self.labels_wperc = self.getPercentLabels()
        plt.rcParams['font.size'] = 8
        self.fig, self.ax = plt.subplots(figsize=(5, 2.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.title_of_small_categories = "Small Groups"

        self.drawChart(labels, data)
        self.widget = self.canvas.get_tk_widget()
        self.widget.grid(row=row, column=col)

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
    
    def drawChart(self, headers, data):
        result_data = self.cleanData(headers, data)
        self.ax.clear()
        wedges, labels, autotexts = self.ax.pie(list(result_data.values()), labels=list(result_data.keys()), autopct="%1.1f%%", textprops={'fontsize': 8}, startangle=90, pctdistance=0.8, labeldistance=1.2)
        self.ax.set_position((-0.05, 0.1, 0.8, 0.8))     # left, bottom, width, height
        self.ax.legend(list(result_data.keys()), loc='center', bbox_to_anchor=(1.75, 0.5))
        self.ax.set_title(self.title)
        self.canvas.draw()

    def cleanData(self, headers, data):
        cleandata = {}
        othercat = 0
        total = 0
        for d in data:
            total += d
        for i,d in enumerate(data):
            if d/total*100 < self.threshold:
                othercat += d
            else:
                cleandata[headers[i]] = d
        if othercat > 0:
            cleandata[self.title_of_small_categories] = othercat
        sorted_dict = dict(sorted(cleandata.items(), key=lambda x: x[1]))
        result = {}
        for i in range(len(sorted_dict)):
            result[list(sorted_dict.items())[-i-1][0]] = list(sorted_dict.items())[-i-1][1]
            result[list(sorted_dict.items())[i][0]] = list(sorted_dict.items())[i][1]
        if len(sorted_dict) %2 == 1:
            middle = list(sorted_dict.keys())[len(sorted_dict)-1]
            result[middle] = sorted_dict[middle]
        return result

class DataTable:
    def __init__(self, window, headers, data, st_row, st_col):
        self.window = window
        self.st_row = st_row
        self.st_col = st_col
        self.table = ttk.Treeview(self.window, height=20)
        self.table.grid(row=st_row, column=st_col)

        if data:
            self.createHeaders(headers, data)
            self.addData(data)
        else:
            self.table["columns"] = ("col1", "col2")
            self.table["show"] = 'headings'
            self.table.column("#0", width=800)

    def drawTree(self, headers, data):
        if data:
            self.table.destroy()
            self.table = ttk.Treeview(self.window, height=20)
            self.table.grid(row=self.st_row, column=self.st_col)
            self.createHeaders(headers, data)
            self.addData(data)

    def createHeaders(self, headers, data):
        self.table["columns"] = headers
        self.table["show"] = 'headings'
        # self.table.heading("#0", text="ID")
        for i,h in enumerate(headers):
            self.table.heading(h, text=h)
            self.table.column(h, anchor='c', width=self.getHeaderSize(i,h,data))

    def addData(self, data):
        for r in data:
            self.table.insert("", 'end', values=(r))

    def getHeaderSize(self, index, header, data):
        multiplier = 8
        length = 0
        for r in data:
            try:
                if len(r[index]) > length:
                    length = len(r[index])
            except TypeError:
                if len(str(r[index])) > length:
                    length = len(str(r[index]))
        if len(header) > length:
            return len(header)*multiplier
        return length*multiplier