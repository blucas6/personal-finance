import tkinter as tk
from tkinter import ttk
import csv

from config import *

class Homepage(tk.Frame):
    def __init__(self, parent, controller):
        self.c = controller
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Home", font=LARGE_FONT).grid(row=0,column=0)
        ttk.Button(self, text="").grid(row=1,column=0)

        self.ReadData()

    def FindStatements(self):
        from os import listdir
        from os.path import isfile, join
        files = [f for f in listdir(STATEMENT_DIR) if isfile(join(STATEMENT_DIR, f))]
        return files

    def ReadData(self):
        files = self.FindStatements()
        if files:
            for f in files:
                with open(STATEMENT_DIR+"/"+f, newline='') as csvfile:
                    datareader = csv.reader(csvfile, delimiter=',')
                    for i,row in enumerate(datareader):
                        if i == 0:
                            self.c.transaction_header = row
                        else:
                            self.c.all_transactions.append(row)