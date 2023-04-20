import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
import os
import csv
from table import DataTable, PieChart

from config import *

class Application:
    def __init__(self, root, controller):
        self.c = controller

        ################ MENU BAR ####################################
        self.menubar = tk.Menu(root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Import Data", command=lambda:[self.c.ImportData()])
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        root.config(menu=self.menubar)
        ##############################################################

        ############### VIEW FILES COLUMN ############################
        self.LeftCol = tk.Frame(root)
        self.LeftCol.grid(row=0, column=0, rowspan=10, sticky='n', padx=5, pady=5)
        tk.Label(self.LeftCol, text="Transaction Files", font=MEDIUM_FONT).grid(row=0,column=0, sticky='n')
        self.listBoxString = tk.StringVar(value=[''])
        self.listBox = tk.Listbox(self.LeftCol, listvariable=self.listBoxString, width=35)
        self.listBox.grid(row=1, column=0, sticky='n')
        ##############################################################

        ############## TRANSACTION MAIN COLUMN #############################
        self.MainCol = tk.LabelFrame(root, text="Your Transactions", bd=10, bg="lightblue", width=10)
        self.MainCol.grid(row=0,column=1, rowspan=10)

        self.transaction_table = DataTable(self.MainCol, self.c.transaction_header, self.c.all_transactions, 1, 1)
        #####################################################################

        ############## ANALYTICS COLUMN #####################################
        self.CurrentData = {}
        self.MonthlySpending = tk.StringVar(value="Total Spent: 0")
        self.RightCol = tk.Frame(root)
        self.RightCol.grid(row=0, column=2, rowspan=10, sticky='n', padx=5, pady=5)

        self.Graph = PieChart(self.RightCol, ["one", "two", "three"], [10, 20, 30], "Monthly Spending")

        self.MonthlySpendingLabel = tk.Label(self.RightCol, textvariable=self.MonthlySpending, font=SMALL_FONT)
        self.MonthlySpendingLabel.grid(row=2, column=0)
        #####################################################################
    
    def setup(self):
        self.c.genListBox()
        self.UpdateChart()
        print(self.CurrentData)

    def RefreshTable(self):
        self.transaction_table = DataTable(self.MainCol, self.c.transaction_header, self.c.all_transactions, 1, 1)

    def UpdateChart(self):
        self.CurrentData = self.c.getPercentages()
        self.Graph = PieChart(self.RightCol, list(self.CurrentData.keys()), list(self.CurrentData.values()), "Monthly Spending")
        total_spending = 0
        for key in self.CurrentData:
            total_spending += self.CurrentData[key]
        self.MonthlySpending.set("Total Spent: %s" % round(total_spending, 2))


