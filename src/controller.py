from config import *
from tkinter import filedialog, messagebox
import tkinter as tk
import shutil
import os
from application import Application
from model import Model
import pandas as pd

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("Personal Finances")
        self.root.geometry("%sx%s"%(WIN_WIDTH, WIN_HEIGHT))
        self.root.resizable()
        #################### DATA VARIABLES ##########################
        self.transaction_header = []    # original column headers from bank
        self.all_transactions = []      # original array of transaction from bank
        self.TotalTransactionsDF = pd.DataFrame()
        self.TotalCategories = []
        ##############################################################
        ################### VIEWING VARIABLES ########################
        self.CurrentViewingMonth = tk.StringVar(value="")
        ##############################################################
        #################### MAIN VARIABLES ##########################
        self.MODEL = Model(self)
        self.VIEW = Application(self.root, self)
        ##############################################################

        self.StartUp()

    def StartUp(self):
        self.LoadInDataTransactions()
        self.TotalCategories = self.MODEL.getAllCategories()
        # print(self.TotalTransactionsDF)
        self.MODEL.FindStartMonth()
        self.VIEW.setup()

    def genListBox(self):
        lst = self.MODEL.FindStatements()
        self.VIEW.listBoxString.set(lst)

    def ImportData(self):
        filename = filedialog.askopenfilenames(initialdir = "/", title = "Select a File", filetypes = (("CSV Files", "*.csv"), ("all files","*.*")))
        for f in filename:
            if self.MODEL.isFileExtCSV(f):
                try:
                    shutil.copy(f, STATEMENT_DIR)
                    shutil.copy(f, CUSTOM_DATA_DIR)
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
                print(f"Error deleting {path}: {e}")
        self.genListBox()
        self.StartUp()