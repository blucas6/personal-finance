import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
import os
import csv
from table import DataTable, PieChart, BarChart
import matplotlib.pyplot as plt


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

        self.transaction_table = ""
        #####################################################################

        ############## ANALYTICS COLUMN #####################################
        self.CurrentData = {}
        self.MonthlySpending_var = tk.StringVar(value="Total Spent: 0")
        self.Graph_Title_var = tk.StringVar(value="Monthly Spending")
        self.RightCol = tk.Frame(root)
        self.RightCol.grid(row=0, column=2, rowspan=10, sticky='n', padx=5, pady=5)
        
        self.GraphTitle = tk.Label(self.RightCol, textvariable=self.Graph_Title_var, font=MEDIUM_FONT)
        self.GraphTitle.grid(row=0, column=0)
        self.Graph = ""

        self.GraphBar = ""

        self.MonthlySpendingLabel = tk.Label(self.RightCol, textvariable=self.MonthlySpending_var, font=SMALL_FONT)
        self.MonthlySpendingLabel.grid(row=2, column=0)

        
        #####################################################################
    
    def setup(self):
        self.c.genListBox()
        self.UpdateCharts()
        print(self.CurrentData)

    def RefreshTable(self):
        self.transaction_table = DataTable(self.MainCol, self.c.transaction_header, self.c.all_transactions, 0, 0)

    def UpdateCharts(self):
        self.CurrentData = self.c.getPercentages()
        self.Graph = PieChart(self.RightCol, list(self.CurrentData.keys()), list(self.CurrentData.values()), 1, 0)
        self.GraphBar = BarChart(self.RightCol, list(self.CurrentData.keys()), list(self.CurrentData.values()), 2, 0, "Categories", "Amount Spent ($)")
        total_spending = 0
        for key in self.CurrentData:
            total_spending += self.CurrentData[key]
        self.MonthlySpending_var.set("Total Spent: %s" % round(total_spending, 2))

    def closeChart(self):
        plt.close()

