from config import *
from tkinter import filedialog
import tkinter as tk
import shutil
from os import listdir
from os.path import isfile, join
from application import Application
import csv
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
        ##############################################################
        #################### MAIN VARIABLES ##########################
        self.MODEL = Model(self)
        self.VIEW = Application(self.root, self)
        ##############################################################

        self.StartUp()

    def StartUp(self):
        self.LoadInDataTransactions()
        print(self.TotalTransactionsDF)
        self.VIEW.setup()

    def genListBox(self):
        lst = self.MODEL.FindStatements()
        self.VIEW.listBoxString.set(lst)

    def ImportData(self):
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("CSV Files", "*.csv"), ("all files","*.*")))
        if self.isFileExtCSV(filename):
            shutil.copy(filename, STATEMENT_DIR)
            shutil.copy(filename, CUSTOM_DATA_DIR)
            self.LoadInDataTransactions()
            self.genListBox()
    
    def LoadInDataTransactions(self):
        self.TotalTransactionsDF = self.MODEL.ReadData()
        self.VIEW.RefreshTable()

    def getPercentages(self):
        return self.MODEL.CalculatePercentages()
    
    def on_closing(self):
        self.root.quit()
        # if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        #     self.VIEW.closeChart()
        #     self.root.quit()
