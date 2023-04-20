from config import *
from tkinter import filedialog
import tkinter as tk
import shutil
from os import listdir
from os.path import isfile, join
from application import Application
import csv
from model import Model

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Personal Finances")
        self.root.geometry("%sx%s"%(WIN_WIDTH, WIN_HEIGHT))
        self.root.resizable()
        #################### DATA VARIABLES ##########################
        self.transaction_header = []    # original column headers from bank
        self.all_transactions = []      # original array of transaction from bank
        ##############################################################
        #################### MAIN VARIABLES ##########################
        self.MODEL = Model(self)
        self.VIEW = Application(self.root, self)
        ##############################################################

        self.LoadInDataTransactions()
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
        self.MODEL.ReadData()
        self.VIEW.RefreshTable()

    def getPercentages(self):
        return self.MODEL.CalculatePercentages()
