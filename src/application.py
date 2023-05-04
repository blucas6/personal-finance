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

        self.AccountFileStrings = []    # list of stringvars

        ################ ICONS ######################################
        self.AddFiles_Icon = ImageTk.PhotoImage(Image.open(ICON_FOLDER+"/open_file.png").resize(ICON_SIZE))
        self.DeleteAllFiles_Icon = ImageTk.PhotoImage(Image.open(ICON_FOLDER+"/delete_file.png").resize(ICON_SIZE))
        self.DeleteFile_Icon = ImageTk.PhotoImage(Image.open(ICON_FOLDER+"/delete_file.png").resize(ICON_SIZE_SMALL))
        self.AddFile_Icon = ImageTk.PhotoImage(Image.open(ICON_FOLDER+"/open_file.png").resize(ICON_SIZE_SMALL))
        self.AddCard_Icon = ImageTk.PhotoImage(Image.open(ICON_FOLDER+"/add_card.png").resize(ICON_SIZE))
        self.DeleteAccount_Icon = ImageTk.PhotoImage(Image.open(ICON_FOLDER+"/delete_account.png").resize(ICON_SIZE_SMALL))

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

        self.AddCardButton = tk.Button(self.ToolBarArea, image=self.AddCard_Icon, command=lambda:self.c.AddNewCard())
        self.AddCardButton.grid(row=0, column=0)
        ##############################################################

        ############### VIEW FILES COLUMN ############################
        self.LeftSideArea = tk.Frame(root)
        self.LeftSideArea.grid(row=1, column=0, rowspan=10, sticky='n', padx=5, pady=5)

        tk.Label(self.LeftSideArea, text="Accounts", font=MEDIUM_FONT).grid(row=0, column=0, sticky='n')
        self.AccountsSubFrame = tk.Frame(self.LeftSideArea, relief='solid', borderwidth=2)
        self.AccountsSubFrame.grid(row=1, column=0, sticky='n')
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
        self.RefreshMonthlyGraphs()
        self.RefreshMonthDropdown()
        self.RefreshTotalSpending()
        self.RefreshAccountListDisplay()

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

    def RefreshAccountListDisplay(self):
        for w in self.AccountsSubFrame.winfo_children():
            w.destroy()
        rw = 0
        self.AccountFileStrings = []
        if bool(self.c.AccountsList.keys()):
            for ind, account in enumerate(self.c.AccountsList.keys()):
                tk.Label(self.AccountsSubFrame, text=account, font=SMALL_FONT).grid(row=rw, column=0)
                tk.Button(self.AccountsSubFrame, image=self.AddFile_Icon, command=lambda account=account:self.c.ImportData(account)).grid(row=rw, column=1)
                tk.Button(self.AccountsSubFrame, image=self.DeleteFile_Icon, command=lambda account=account:self.c.DeleteCardFiles(account)).grid(row=rw, column=2)
                tk.Button(self.AccountsSubFrame, image=self.DeleteAccount_Icon, command=lambda account=account:self.c.DeleteAccount(account)).grid(row=rw, column=3)

                files = self.c.AccountsList[account]
                print(self.c.AccountsList[account])
                if files:
                    self.AccountFileStrings.append(tk.StringVar(value=files))
                    tk.Listbox(self.AccountsSubFrame, listvariable=self.AccountFileStrings[ind], width=35, height=len(files)).grid(row=rw+1, column=0)
                else:
                    self.AccountFileStrings.append(tk.StringVar(value=['No Files']))
                    tk.Listbox(self.AccountsSubFrame, listvariable=self.AccountFileStrings[ind], width=35, height=1).grid(row=rw+1, column=0)
                rw += 2
        else:
            tk.Label(self.AccountsSubFrame, text="No Accounts Added", font=SMALL_FONT).grid(row=rw, column=0)
