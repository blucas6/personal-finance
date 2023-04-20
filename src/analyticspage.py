import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from config import *

class AnalyticsPage(tk.Frame):
    def __init__(self, parent, controller):
        self.c = controller
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Analytics", font=LARGE_FONT).grid(row=0,column=0)

        self.Trans_Dict = {}
        self.Categories = []
        self.Percentage = []

        self.SetupData()
        self.RefreshPie()

    def RefreshPie(self):
        f = Figure()
        axis = f.add_subplot(111)
        axis.pie(self.Percentage, radius=1, labels=self.Categories,autopct='%0.2f%%', shadow=True)
        axis.axis("equal")
        chart = FigureCanvasTkAgg(f, self)
        chart.draw()
        chart.get_tk_widget().grid(row=0, column=0)

    def SetupData(self):
        categories = []
        percentage = []
        if self.c.all_transactions:
            for t in self.c.all_transactions:
                if t[PRICE_INDEX]:
                    if not t[CATEGORY_INDEX] in self.Trans_Dict:
                        self.Trans_Dict[t[CATEGORY_INDEX]] = float(t[PRICE_INDEX])
                    else:
                        self.Trans_Dict[t[CATEGORY_INDEX]] += float(t[PRICE_INDEX])
            categories = list(self.Trans_Dict.keys())
            total_spending = 0
            for key in self.Trans_Dict:
                total_spending += self.Trans_Dict[key]
            for key in self.Trans_Dict:
                percentage.append(self.Trans_Dict[key] / total_spending * 100)
            
            return categories, percentage

    def Reorder(self):
        categories, percentage = self.SetupData()
        # take random 
