from config import *
from tkinter import filedialog
import shutil
from os import listdir
from os.path import isfile, join
from application import Application
import csv
import pandas as pd
from datetime import datetime
import configparser

class Model:
    def __init__(self, controller):
        self.c = controller

    def FindStartMonth(self):
        try:
            earliest = self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX].min()
            self.c.CurrentViewingMonth.set(pd.to_datetime(earliest).strftime("%B %Y"))
        except:
            self.c.CurrentViewingMonth.set("No Transactions Available")

    def FindStatements(self):
        files = [f for f in listdir(STATEMENT_DIR) if isfile(join(STATEMENT_DIR, f))]
        return files
    
    def CleanDates(self, df):
        df[TRANSACTIONDATE_INDEX] = pd.to_datetime(df[TRANSACTIONDATE_INDEX])
        df[DATEPOSTED_INDEX] = pd.to_datetime(df[DATEPOSTED_INDEX])
        return df
    
    def ReadData(self):
        list_of_dfs = []
        files = self.FindStatements()
        merged_dfs = pd.DataFrame()
        if files:
            for f in files:
                list_of_dfs.append(pd.read_csv(CUSTOM_DATA_DIR+"/"+f))
            merged_dfs = pd.concat(list_of_dfs, ignore_index=True)
            merged_dfs = merged_dfs.iloc[::-1].reset_index(drop=True)
        return merged_dfs

    def isFileExtCSV(self, f):
        if f[-1] == 'v' and f[-2] == 's' and f[-3] == 'c' and f[-4] == '.':
            return True
        return False
    
    def getPercentages(self, transactions):
        if transactions.empty:
            return {}
        groups = transactions.groupby(CATEGORY_INDEX)
        CurrentData = {}
        for name, group in groups:
            sum = group[PAYMENT_INDEX].sum()
            CurrentData[name] = sum
        for cat in self.c.TotalCategories:
            if not cat in CurrentData:
                CurrentData[cat] = 0
        ordered = {}
        for cat in self.c.TotalCategories:
            ordered[cat] = CurrentData[cat]
        return ordered
    
    def getTransactionsWithinRange(self):
        if self.c.TotalTransactionsDF.empty:
            return self.c.TotalTransactionsDF
        dt = datetime.strptime(self.c.CurrentViewingMonth.get(), '%B %Y')
        monthrange = ((pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.month == dt.month) & (pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.year == dt.year))
        return self.c.TotalTransactionsDF[monthrange]
    
    def getMonthGroups(self):
        if self.c.TotalTransactionsDF.empty:
            return self.c.TotalTransactionsDF
        return self.c.TotalTransactionsDF.groupby([pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.month, pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.year])

    def getAvailableMonths(self):
        if self.c.TotalTransactionsDF.empty:
            return [""]
        months = []
        groups = self.getMonthGroups()
        for name, group in groups:
            months.append(datetime.strptime(str(name), "(%m, %Y)").strftime("%B %Y"))
        return sorted(months, key=lambda x: self.StringToDatetime(x))
    
    def getTotalSpending(self):
        if self.c.TotalTransactionsDF.empty:
            return {}
        monthlyspending = {}
        groups = self.getMonthGroups()
        for name, group in groups:
            monthlyspending[datetime.strptime(str(name), "(%m, %Y)").strftime("%B %y")] = group[PAYMENT_INDEX].sum()
        return dict(sorted(monthlyspending.items(), key=lambda x: self.StringToDatetime(x[0], False)))

    def StringToDatetime(self, string, bigyear=True):
        if bigyear:
            return datetime.strptime(string, '%B %Y')
        return datetime.strptime(string, '%B %y')
    
    def getAllCategories(self):
        cats = []
        if self.c.TotalTransactionsDF.empty:
            return []
        groups = self.c.TotalTransactionsDF.groupby(CATEGORY_INDEX)
        for name, group in groups:
            cats.append(name)
        return cats
    
    def ReadFileFindColumns(self, file):
        return pd.read_csv(file).columns
    
    def AddSectionorValueToConfig(self, section, param="", value=""):
        if not self.c.Parameters.has_section(section):
            self.c.Parameters.add_section(section)
        if param:
            if value:
                if isinstance(value, list):
                    if len(value) == 1:
                        val = str(value[0])
                    else:
                        val = ','.join(value)
                else:
                    val = value
                self.c.Parameters.set(section, param, val)
            else:
                self.c.Parameters.set(section, param, "")
        self.WriteToConfig()

    def WriteToConfig(self):
        with open(PARAMETER_FILE, 'w') as pfile:
            self.c.Parameters.write(pfile)

    def RemoveSectionFromConfig(self, section):
        if self.c.Parameters.has_section(section):
            self.c.Parameters.remove_section(section)
            self.WriteToConfig()

