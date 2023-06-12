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
import numpy as np

class Model:
    def __init__(self, controller):
        self.c = controller

    def FindStartMonth(self):
        try:
            earliest = self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX].min()
            self.c.CurrentViewingMonth.set(pd.to_datetime(earliest).strftime("%B %Y"))
        except Exception as e:
            print("Couldn't find start month:", e)
            self.c.CurrentViewingMonth.set("No Transactions Available")
    
    def CleanDate(self, value):
        return pd.to_datetime(value).strftime("%Y-%m-%d")
    
    def UndoNegatives(self, value):
        if value < 0:
            return value*-1
        return value
        
    def CheckSetup(self, file, account):
        ex = pd.read_csv(file)
        for name in DT_COLUMN_NAMES:
            if self.c.Parameters[account][name] != 'None' and self.c.Parameters[account][name] != ' ' and self.c.Parameters[account][name] != '':
                if not self.c.Parameters[account][name] in ex.columns:
                    return False
        return True 
    
    def CreateCleanTable(self, rawdt, account):
        columnswewant = []
        rename = []
        columnsnotincluded = []
        # loop through all column names for the datatable 
        for cww in DT_COLUMN_NAMES:
            # if found a matching setting, append that column to the clean data
            if cww in self.c.Parameters[account] and self.c.Parameters[account][cww] != '':
                columnswewant.append(self.c.Parameters[account][cww])
                rename.append(cww)
            # if not found, add empty column later
            else:
                columnsnotincluded.append(cww)
        print("COLUMNS WE WANT:",columnswewant)
        # copy whatever data was setup
        cleandt = rawdt[columnswewant].copy()
        # add in empty columns for data not setup
        for cni in columnsnotincluded:
            cleandt[cni] = " "
        # rename columns to the appropriate names IN ORDER 
        rename = rename + columnsnotincluded
        cleandt.columns = rename
        # check if the payment column has combined credit and debit
        if self.c.Parameters[account][COMBINED_PARAMETER]:
            # separate the values by positivity
            cleandt[CREDIT_INDEX] = cleandt[PAYMENT_INDEX][cleandt[PAYMENT_INDEX] > 0]
            cleandt[PAYMENT_INDEX] = cleandt[PAYMENT_INDEX][cleandt[PAYMENT_INDEX] < 0]
            cleandt[PAYMENT_INDEX] = cleandt[PAYMENT_INDEX].apply(self.UndoNegatives)
        # clean date format
        cleandt[TRANSACTIONDATE_INDEX] = cleandt[TRANSACTIONDATE_INDEX].apply(self.CleanDate)
        # replace NaNs in money columns with 0s
        cleandt[PAYMENT_INDEX] = cleandt[PAYMENT_INDEX].fillna(0)
        cleandt[CREDIT_INDEX] = cleandt[CREDIT_INDEX].fillna(0)
        # replace others NaNs with blanks
        cleandt = cleandt.fillna('')
        # reorder columns
        cleandt = cleandt.reindex(columns=DT_COLUMN_NAMES)
        return cleandt
    
    def ReadData(self):
        list_of_dfs = []
        merged_dfs = pd.DataFrame() 
        for account, flist in self.c.AccountsFileList.items():
            for f in flist:
                if f != "" and f != " " and self.c.Parameters[account][SETUP_PARAMETER]:
                    filestring = STATEMENT_DIR+"/"+account+"/"+f
                    print("FILE TO READ", filestring)
                    try:
                        singledf = pd.read_csv(filestring)
                    except Exception as e:
                        print("No file", filestring)
                        print(e)
                    else:
                        cleandf = self.CreateCleanTable(singledf, account)
                        list_of_dfs.append(cleandf)
        if list_of_dfs:
            merged_dfs = pd.concat(list_of_dfs, ignore_index=True)
            merged_dfs = merged_dfs.iloc[::-1].reset_index(drop=True)
            # rearrange by date
            merged_dfs = merged_dfs.sort_values(TRANSACTIONDATE_INDEX)
        return merged_dfs

    def isFileExtCSV(self, f):
        if f[-1] == 'v' and f[-2] == 's' and f[-3] == 'c' and f[-4] == '.':
            return True
        if f[-1] == 'V' and f[-2] == 'S' and f[-3] == 'C' and f[-4] == '.':
            return True
        return False
    
    def getPercentages(self, transactions):
        if transactions.empty:
            return {}
        # should replace empty categories with NaN then drop NaNs from groupby, (it doesnt)
        transactions = transactions.replace('', np.nan).dropna(subset=[CATEGORY_INDEX], inplace=False)
        groups = transactions.groupby(CATEGORY_INDEX)
        CurrentData = {}
        print("GROUPBY")
        for name, group in groups:
            # if empty category, skip
            if name == ' ':
                continue
            sum = group[PAYMENT_INDEX].sum()
            CurrentData[name] = sum
        # check if there is any data to graph
        if CurrentData: 
            for cat in self.c.TotalCategories:
                if not cat in CurrentData:
                    CurrentData[cat] = 0
            ordered = {}
            for cat in self.c.TotalCategories:
                ordered[cat] = CurrentData[cat]
            return ordered
        return {}
    
    def getTransactionsWithinRange(self):
        if self.c.TotalTransactionsDF.empty:
            return self.c.TotalTransactionsDF
        # dt = datetime.strptime(self.c.CurrentViewingMonth.get(), '%B %Y')
        dt = self.StringToDatetime(self.c.CurrentViewingMonth.get())
        monthrange = ((pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.month == dt.month) & (pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.year == dt.year))
        print("-getting transactions within range-\n", self.c.TotalTransactionsDF[monthrange])
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
    
    def ReadFileFindColumnsAndFirstRow(self, file):
        df = pd.read_csv(file)
        return df.columns, df.iloc[0].values.tolist()
    
    def AddSectionorValueToConfig(self, section, param="", value=""):
        if not self.c.Parameters.has_section(section):
            self.c.Parameters.add_section(section)
        if param:
            if value:
                if isinstance(value, list):
                    value = [x for x in value if x]
                    if len(value) == 1:
                        val = value[0]
                    else:
                        val = ",".join(value)
                elif isinstance(value, bool):
                    val = str(value)
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

