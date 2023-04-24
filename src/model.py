from config import *
from tkinter import filedialog
import shutil
from os import listdir
from os.path import isfile, join
from application import Application
import csv
import pandas as pd
from datetime import datetime

class Model:
    def __init__(self, controller):
        self.c = controller

    def FindStartMonth(self):
        earliest = self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX].min()
        self.c.CurrentViewingMonth.set(pd.to_datetime(earliest).strftime("%B %Y"))

    def FindStatements(self):
        files = [f for f in listdir(CUSTOM_DATA_DIR) if isfile(join(CUSTOM_DATA_DIR, f))]
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
            # merged_dfs = self.CleanDates(merged_dfs)
            merged_dfs = merged_dfs.iloc[::-1].reset_index(drop=True)
            # DELETE LATER #
            for f in files:
                with open(CUSTOM_DATA_DIR+"/"+f, newline='') as csvfile:
                    datareader = csv.reader(csvfile, delimiter=',')
                    for i,row in enumerate(datareader):
                        if i == 0:
                            self.c.transaction_header = row
                        else:
                            self.c.all_transactions.append(row)
            ###########################
        return merged_dfs

    def isFileExtCSV(self, f):
        for c in range(len(f)):
            if f[c] == '.':
                if f[c+1] == 'c' and f[c+2] == 's' and f[c+3] == 'v' and c+4 > len(f)-1:
                    return True
        return False
    
    def getPercentages(self, transactions):
        groups = transactions.groupby(CATEGORY_INDEX)
        CurrentData = {}
        for name, group in groups:
            sum = group[PAYMENT_INDEX].sum()
            CurrentData[name] = sum
        return CurrentData
    
    def getTransactionsWithinRange(self):
        dt = datetime.strptime(self.c.CurrentViewingMonth.get(), '%B %Y')
        monthrange = ((pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.month == dt.month) & (pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.year == dt.year))
        return self.c.TotalTransactionsDF[monthrange]
    
    def getAvailableMonths(self):
        months = []
        groups = self.c.TotalTransactionsDF.groupby([pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.month, pd.to_datetime(self.c.TotalTransactionsDF[TRANSACTIONDATE_INDEX]).dt.year])
        for name, group in groups:
            months.append(datetime.strptime(str(name), "(%m, %Y)").strftime("%B %Y"))
        return months