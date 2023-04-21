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

    def FindStatements(self):
        files = [f for f in listdir(CUSTOM_DATA_DIR) if isfile(join(CUSTOM_DATA_DIR, f))]
        return files
    
    def ReadData(self):
        list_of_dfs = []
        files = self.FindStatements()
        merged_dfs = pd.DataFrame()
        if files:
            for f in files:
                list_of_dfs.append(pd.read_csv(CUSTOM_DATA_DIR+"/"+f))
            merged_dfs = pd.concat(list_of_dfs, ignore_index=True)
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
    
    def CalculatePercentages(self):
        if self.c.all_transactions:
            sort = {}
            CurrentData = {}
            for t in self.c.all_transactions:
                if t[PRICE_INDEX]:
                    if not t[CATEGORY_INDEX] in CurrentData:
                        sort[t[CATEGORY_INDEX]] = float(t[PRICE_INDEX])
                    else:
                        sort[t[CATEGORY_INDEX]] += float(t[PRICE_INDEX])
            sort = dict(sorted(sort.items(), key=lambda item: item[1]))
            keys = list(sort.keys())
            for i,k in enumerate(keys):
                if not k in CurrentData:
                    CurrentData[k] = sort[k]
                    opposite_key = keys[len(keys)-1-i]
                    CurrentData[opposite_key] = sort[opposite_key]
        return CurrentData