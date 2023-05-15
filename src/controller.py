from config import *
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk
import shutil
import os
from application import Application
from model import Model
import pandas as pd
from optionwindow import AccountSetupWindow
import configparser
from collections import defaultdict

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
        self.AccountsFileList = defaultdict(list)   # { account: [trans1, trans2, ...] } holds files per account
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
            print("Section:", section)
            self.AccountsFileList[section]
            for key, value in self.Parameters.items(section):
                print("Parameters:", key, value)
                if key == "files":
                    self.AccountsFileList[section] = value.split(",")

    def StartUp(self):
        self.ReadFromConfig()
        self.TotalTransactionsDF = self.MODEL.ReadData()
        self.TotalCategories = self.MODEL.getAllCategories()
        self.MODEL.FindStartMonth()
        self.VIEW.setup()

    def ImportData(self, account):
        filenames = list(filedialog.askopenfilenames(initialdir = "/Downloads", title = "Select a File", filetypes = (("CSV Files", "*.csv"), ("all files","*.*"))))
        for f in filenames:
            cols = self.MODEL.ReadFileFindColumns(f)
            AccountSetupWindow(self.root, self, cols, account)
            if self.MODEL.isFileExtCSV(f):
                try:
                    shutil.copy(f, STATEMENT_DIR)
                    shutil.copy(f, CUSTOM_DATA_DIR)
                except:
                    messagebox.showerror(title="Import Error", message="Failed to import file: %s"%f)
                if self.AccountsFileList[account]:
                    self.AccountsFileList[account].append(f)
                else:
                    self.AccountsFileList[account] = [f]
            else:
                messagebox.showerror(title="File Type Error", message="File is not a .csv!")
        self.AddSectionorValueToConfig(account, 'Files', self.AccountsFileList[account])
        self.StartUp()

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

    def DeleteCardFiles(self, account):
        files = self.AccountsFileList[account]
        paths = []
        for f in files:
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
        self.AddSectionorValueToConfig(account, "files")
        self.StartUp()

    def AddNewCard(self):
        cardname = simpledialog.askstring(title="Add Account", prompt="Enter the name for the account you would like to add:")
        if cardname:
            self.AccountsFileList[cardname] = []
            self.VIEW.RefreshAccountListDisplay()
            self.AddSectionorValueToConfig(cardname)

    def DeleteAccount(self, account):
        print(f"Deleting {account}")
        self.DeleteCardFiles(account)
        del self.AccountsFileList[account]
        self.MODEL.RemoveSectionFromConfig(account)
        self.StartUp()

    def AddSectionorValueToConfig(self, section, param="", value=""):
        self.MODEL.AddSectionorValueToConfig(section=section, param=param, value=value)
