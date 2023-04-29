import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
import os
import csv
from table import DataTable, PieChart, BarChart
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from PIL import ImageTk, Image

from config import *

class Application:
    def __init__(self, root, controller):
        self.c = controller

        ################ ICONS ######################################
        self.AddFileIcon = ImageTk.PhotoImage(Image.open("../icons/open_file.png").resize((23,23)))
        self.DeleteAllFiles = ImageTk.PhotoImage(Image.open("../icons/delete_file.png").resize((23,23)))
        #############################################################

        ################ MENU BAR ####################################
        self.menubar = tk.Menu(root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Import Data", command=lambda:[self.c.ImportData()])
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        root.config(menu=self.menubar)
        ##############################################################

        ############## TOOL BAR ######################################
        self.ToolBarArea = tk.Frame(root)
        self.ToolBarArea.grid(row=0, column=0, columnspan=3, sticky='w')
        self.AddFileButton = tk.Button(self.ToolBarArea, image=self.AddFileIcon, command=lambda:self.c.ImportData())
        self.AddFileButton.grid(row=0, column=0)
        self.DeleteAllFilesButton = tk.Button(self.ToolBarArea, image=self.DeleteAllFiles, command=lambda:self.c.DeleteAllImportedFiles())
        self.DeleteAllFilesButton.grid(row=0, column=1)
        ##############################################################

        ############### VIEW FILES COLUMN ############################
        self.LeftSideArea = tk.Frame(root)
        self.LeftSideArea.grid(row=1, column=0, rowspan=10, sticky='n', padx=5, pady=5)
        tk.Label(self.LeftSideArea, text="Transaction Files", font=MEDIUM_FONT).grid(row=0,column=0, sticky='n')
        self.listBoxString = tk.StringVar(value=[''])
        self.listBox = tk.Listbox(self.LeftSideArea, listvariable=self.listBoxString, width=35)
        self.listBox.grid(row=1, column=0, sticky='n')
        ##############################################################

        ############## TRANSACTION MAIN COLUMN #############################
        self.MainArea = tk.Frame(root)
        self.MainArea.grid(row=1,column=1, sticky='n')

        self.MonthlyDropDown = ttk.Combobox(self.MainArea)
        self.MonthlyDropDown.set('Select a Month')
        self.MonthlyDropDown.grid(row=0, column=0, sticky='w')
        self.MonthlyDropDown.bind("<<ComboboxSelected>>", self.DropDownEvent)
        self.CurrentMonthTitle_label = tk.Label(self.MainArea, textvariable=self.c.CurrentViewingMonth, font=LARGE_FONT)
        self.CurrentMonthTitle_label.grid(row=0, column=1, columnspan=3)

        self.transactionFrame = tk.LabelFrame(self.MainArea, text="Your Transactions", bd=10, bg="lightblue", width=10)
        self.transactionFrame.grid(row=2, column=0, columnspan=4)
        self.transaction_table = DataTable(self.transactionFrame, [], [], 1, 0)

        self.TotalSpendingGraphTitle = tk.StringVar(value="Total Spending")
        self.TotalSpendingGraph_Label = tk.Label(self.MainArea, textvariable=self.TotalSpendingGraphTitle, font=MEDIUM_FONT)
        self.TotalSpendingGraph_Label.grid(row=3, column=0, columnspan=4)
        self.TotalSpendingGraph = BarChart(self.MainArea, [], [], 4, 0, "Months", "Amount Spend($)", [6, 2], columnspan=4)


        #####################################################################

        ############## ANALYTICS COLUMN #####################################
        self.CurrentData = {}
        self.MonthlySpending_var = tk.StringVar(value="Total Spent: 0")
        self.Graph_Title_var = tk.StringVar(value="Monthly Spending")
        self.RightSideArea = tk.Frame(root)
        self.RightSideArea.grid(row=1, column=2, rowspan=10, sticky='n', padx=5, pady=5)
        
        self.GraphTitle = tk.Label(self.RightSideArea, textvariable=self.Graph_Title_var, font=MEDIUM_FONT)
        self.GraphTitle.grid(row=0, column=0)
        self.Graph = PieChart(self.RightSideArea, [], [], 1, 0)

        self.GraphBar = BarChart(self.RightSideArea, [], [], 2, 0, "Categories", "Amount Spent ($)", [5, 2.5])
        self.MonthlySpendingLabel = tk.Label(self.RightSideArea, textvariable=self.MonthlySpending_var, font=SMALL_FONT)
        self.MonthlySpendingLabel.grid(row=3, column=0)


        
        #####################################################################
    
    def setup(self):
        self.c.genListBox()
        self.RefreshMonthlyGraphs()
        self.RefreshMonthDropdown()
        self.RefreshTotalSpending()

    def RefreshMonthlyGraphs(self):
        transactions = self.c.getTransactionsWithinRange()
        self.transaction_table.drawTree(list(transactions.columns), transactions.values.tolist())
        CurrentData = self.c.getPercentages(transactions)
        self.Graph.drawChart(list(CurrentData.keys()), list(CurrentData.values()))
        self.GraphBar.drawChart(list(CurrentData.keys()), list(CurrentData.values()))
        total_spending = 0
        for key in CurrentData:
            total_spending += CurrentData[key]
        self.MonthlySpending_var.set("Total Spent: %s" % round(total_spending, 2))

    def RefreshTotalSpending(self):
        CurrentData = self.c.FindTotalSpending()
        try:
            currentmonth = datetime.strptime(self.c.CurrentViewingMonth.get(), '%B %Y').strftime('%B %y')
        except:
            currentmonth = 'No Transactions Available'
        colors = []
        for key in CurrentData.keys():
            if currentmonth == key:
                colors.append('#2ca02c')
            else:
                colors.append('#1f77b4')
        self.TotalSpendingGraph.drawChart(list(CurrentData.keys()), list(CurrentData.values()), colors=colors)

    def RefreshMonthDropdown(self):
        combo = self.c.FindAvailableMonths()
        self.MonthlyDropDown['values'] = combo
        self.MonthlyDropDown.current(0)

    def closeCharts(self):
        if not self.TotalSpendingGraph == "":
            self.TotalSpendingGraph.widget.destroy()
        if not self.Graph == "":
            self.Graph.widget.destroy()
        if not self.GraphBar == "":
            self.GraphBar.widget.destroy()

    def DropDownEvent(self, e):
        self.c.ChangeView(self.MonthlyDropDown.get())
        self.RefreshTotalSpending()
        
