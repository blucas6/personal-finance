from config import *
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk
import shutil
import os
from application import Application
from model import Model
import pandas as pd
from optionwindow import OptionWindow
import configparser

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("Personal Finances")
        self.root.geometry("%sx%s"%(WIN_WIDTH, WIN_HEIGHT))
        self.root.resizable()
        #################### DATA VARIABLES ##########################
        self.Parameters = configparser.ConfigParser()
        self.TotalTransactionsDF = pd.DataFrame()
        self.TotalCategories = []
        self.AccountsList = {}
        ##############################################################
        ################### VIEWING VARIABLES ########################
        self.CurrentViewingMonth = tk.StringVar(value="")
        ##############################################################
        #################### MAIN VARIABLES ##########################
        self.MODEL = Model(self)
        self.VIEW = Application(self.root, self)
        ##############################################################

        self.StartUp()

    def ReadFromConfig(self):
        self.Parameters.read(PARAMETER_FILE)
        for section in self.Parameters.sections():
            self.AccountsList[section] = ""
        for op_name, op_val in self.Parameters.items():
            print(op_name, op_val)

    def StartUp(self):
        self.ReadFromConfig()
        self.LoadInDataTransactions()
        self.TotalCategories = self.MODEL.getAllCategories()
        self.MODEL.FindStartMonth()
        self.VIEW.setup()

    def ImportData(self, account):
        filename = filedialog.askopenfilenames(initialdir = "/Downloads", title = "Select a File", filetypes = (("CSV Files", "*.csv"), ("all files","*.*")))
        for f in filename:
            # cols = self.MODEL.ReadFileFindColumns(f)
            # OptionWindow(self.root, f, cols, cardname, 'Category', "Select which column dictates the Categories column. This is where your transactions are categorized by the types of purchases.")
            # OptionWindow(self.root, f, cols, cardname, 'Price', "Select which column dictates the Price column. This is the amount you paid for the transaction.")
            # OptionWindow(self.root, f, cols, cardname, 'Transaction Date', "Select which column dictates the Transaction Date column. This is the original data of the transaction.")
            # OptionWindow(self.root, f, cols, cardname, 'Posted Date', "Select which column dictates the Posted Data column. This is the date the transaction was posted to your account.")
            
            if self.MODEL.isFileExtCSV(f):
                try:
                    shutil.copy(f, STATEMENT_DIR)
                    shutil.copy(f, CUSTOM_DATA_DIR)
                    self.AccountsList[account].append(filename)
                    self.MODEL.AddSectionorValueToConfig(account, 'Files', filename)
                    self.StartUp()
                except:
                    messagebox.showerror(title="Import Error", message="Failed to import file: %s"%f)
            else:
                messagebox.showerror(title="File Type Error", message="File is not a .csv!")

    def LoadInDataTransactions(self):
        self.TotalTransactionsDF = self.MODEL.ReadData()

    def getPercentages(self, transactions):
        return self.MODEL.getPercentages(transactions)
    
    def on_closing(self):
        self.root.quit()
        # if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        #     self.VIEW.closeChart()
        #     self.root.quit()

    def getTransactionsWithinRange(self):
        return self.MODEL.getTransactionsWithinRange()
    
    def FindAvailableMonths(self):
        return self.MODEL.getAvailableMonths()
    
    def ChangeView(self, date):
        self.CurrentViewingMonth.set(date)
        self.VIEW.RefreshMonthlyGraphs()

    def FindTotalSpending(self):
        return self.MODEL.getTotalSpending()

    def FindAllCategories(self):
        self.MODEL.getAllCategories()

    def DeleteAllImportedFiles(self):
        paths = []
        for f in os.listdir(STATEMENT_DIR):
            paths.append(os.path.join(STATEMENT_DIR, f))
        for f in os.listdir(CUSTOM_DATA_DIR):
            paths.append(os.path.join(CUSTOM_DATA_DIR, f))
        for path in paths:
            try:
                if os.path.isfile(path):
                    os.remove(path)
            except Exception as e:
                messagebox.showerror(title="Deletion Error", message=f"Error deleting {path}: {e}")
        self.genListBox()
        self.StartUp()

    def AddNewCard(self):
        cardname = simpledialog.askstring(title="Add Account", prompt="Enter the name for the account you would like to add:")
        if cardname:
            self.AccountsList[cardname] = []
            self.VIEW.RefreshAccountListDisplay()
            self.MODEL.AddSectionorValueToConfig(cardname)

    def DeleteAccount(self, account):
        print(f"Deleting {account}")
        del self.AccountsList[account]
        self.VIEW.RefreshAccountListDisplay()
        self.MODEL.RemoveSectionFromConfig(account)