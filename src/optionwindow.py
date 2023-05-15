import tkinter as tk
from config import *
import configparser

class AccountSetupWindow:
    def __init__(self, root, controller, cols, cardname):
        self.c = controller
        self.columns = cols
        self.card_name = cardname
        self.window = tk.Toplevel(root)
        self.window.title("Account Setup")

        self.SettingsCollection = {}   # dict of all column indexes { index_value: 'column_name' }

        self.TopArea = tk.Frame(self.window)
        self.TopArea.grid(row=0, column=0, columnspan=2)
        tk.Label(self.TopArea, text="CSV Format Setup", font=MEDIUM_FONT).grid(row=0, column=0, padx=20)
        tk.Label(self.TopArea, text="Which of these columns is responsible for...", font=SMALL_FONT).grid(row=1, column=0, pady=(25, 5))

        self.MiddleArea = tk.Frame(self.window)
        self.MiddleArea.grid(row=1, column=0)

        self.CategoryArea = tk.Frame(self.MiddleArea)
        self.CategoryArea.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.FillSelectionArea(self.CategoryArea, 'category', 'category')
        self.PaymentArea = tk.Frame(self.MiddleArea)
        self.PaymentArea.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.FillSelectionArea(self.PaymentArea, 'payment', 'payment')
        self.TransactionDateArea = tk.Frame(self.MiddleArea)
        self.TransactionDateArea.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.FillSelectionArea(self.TransactionDateArea, 'transaction date', 'transactiondate')
        self.PostedDateArea = tk.Frame(self.MiddleArea)
        self.PostedDateArea.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        self.FillSelectionArea(self.PostedDateArea, 'posted date', 'posteddate')
        self.CreditArea = tk.Frame(self.MiddleArea)
        self.CreditArea.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.FillSelectionArea(self.CreditArea, 'credit', 'credit')
        self.IncomeArea = tk.Frame(self.MiddleArea)
        self.IncomeArea.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(self.IncomeArea, text="Does the").grid(row=0, column=0)
        tk.Label(self.IncomeArea, text="credit", font=ITALIC_FONT).grid(row=1, column=0)
        tk.Label(self.IncomeArea, text="section of this account count as income?").grid(row=2, column=0)
        self.SettingsCollection['income'] = tk.BooleanVar()
        tk.Checkbutton(self.IncomeArea, text="Yes, this account has income", variable=self.SettingsCollection['income']).grid(row=3, column=0, pady=10, columnspan=3)
        
        self.BottomArea = tk.Frame(self.window)
        self.BottomArea.grid(row=2, column=0, columnspan=2)
        tk.Button(self.BottomArea, text="Submit", command=lambda:[self.SubmitSettings()]).grid(row=0, column=0, padx=3, pady=3)

        self.window.wait_window()

    def FillSelectionArea(self, frame, italics, dict_index):
        tk.Label(frame, text="describing the").grid(row=0, column=0, sticky='w')
        tk.Label(frame, text=italics, font=ITALIC_FONT).grid(row=0, column=1, sticky='w')
        tk.Label(frame, text="of a purchase?").grid(row=0, column=2, sticky='w')
        self.SettingsCollection[dict_index] = tk.StringVar()
        for r,c in enumerate(self.columns):
            tk.Radiobutton(frame, text=c, variable=self.SettingsCollection[dict_index], value=c).grid(row=r+1, column=0, sticky='w', padx=15, columnspan=3)


    def SubmitSettings(self):
        for key in self.SettingsCollection.keys():
            print("SAVING:", self.card_name, key, self.SettingsCollection[key].get())
            self.c.AddSectionorValueToConfig(section=self.card_name, param=key, value=self.SettingsCollection[key].get())

        self.window.destroy()