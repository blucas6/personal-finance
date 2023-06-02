import tkinter as tk
from config import *
import configparser
from tkinter import ttk

class AccountSetupWindow:
    def __init__(self, root, controller, cols, cardname, firstrow, filename):
        self.c = controller
        self.columns = cols
        self.firstrow = firstrow
        self.card_name = cardname
        self.window = tk.Toplevel(root)
        self.window.title("Account Setup")
        self.window.protocol("WM_DELETE_WINDOW", self.Cancel)

        self.CombinedPayCredit_str = 'Payment & Income'
        self.AccountFeaturesIncome = tk.IntVar(value=0)
        self.SettingsCollection = {}   # dict of all column indexes { config_file_param : 'column_name' }

        for cfp in DT_COLUMN_NAMES:
            self.SettingsCollection[cfp] = tk.StringVar(value='None')
        self.SettingsCollection[self.CombinedPayCredit_str] = tk.StringVar(value='None')
        self.dropdownoptions = [' ']
        for option in DT_COLUMN_NAMES:
            self.dropdownoptions.append(option)
        self.dropdownoptions.append(self.CombinedPayCredit_str)

        self.TopArea = tk.Frame(self.window)
        self.TopArea.grid(row=0, column=0)
        tk.Label(self.TopArea, text="CSV Format Setup", font=MEDIUM_FONT).grid(row=0, column=0, padx=20, columnspan=2)
        tk.Label(self.TopArea, text="Select the what each column represents, leave columns as None for other information.", font=SMALL_FONT).grid(row=1, column=0, sticky='e', pady=(25, 5), columnspan=2)
        tk.Label(self.TopArea, text='Showing example row from: ', font=SMALL_FONT).grid(row=2, column=0, pady=10)
        tk.Label(self.TopArea, text=filename, font=ITALIC_SMALL_FONT).grid(row=2, column=1)
        self.MiddleArea = tk.Frame(self.window)
        self.MiddleArea.grid(row=1, column=0)

        self.CategoryArea = tk.Frame(self.MiddleArea)
        self.CategoryArea.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.dropdowns = {}
        for ind,col in enumerate(self.columns):
            tk.Label(self.CategoryArea, text=col, font=ITALIC_FONT).grid(row=ind, column=0)
            tk.Label(self.CategoryArea, text='(ex. '+str(self.firstrow[ind])+')', font=SMALL_FONT).grid(row=ind, column=1)
            self.dropdowns[col] = ttk.Combobox(self.CategoryArea, values=self.dropdownoptions, state="readonly")
            self.dropdowns[col].grid(row=ind, column=2)

        self.BottomArea = tk.Frame(self.window)
        self.BottomArea.grid(row=2, column=0)
        tk.Checkbutton(self.BottomArea, text='Yes, this account holds income:', variable=self.AccountFeaturesIncome).grid(row=0, column=0)
        tk.Button(self.BottomArea, text="Submit", command=lambda:[self.SubmitSettings()]).grid(row=0, column=1, padx=10, pady=10)

        self.window.wait_window()

    def SubmitSettings(self):
        print(self.dropdowns)
        config_params = DT_COLUMN_NAMES + [COMBINED_PARAMETER]
        for csv_col, combo in self.dropdowns.items():
            assoc_param = combo.get()
            if assoc_param != 'None' and assoc_param != ' ' and assoc_param != '':
                print("SAVING: ", csv_col, assoc_param)
                if assoc_param == self.CombinedPayCredit_str:
                    # if combined parameter is used, set flag in config, add csv column name to the payment parameter in config
                    self.c.AddSectionorValueToConfig(section=self.card_name, param=COMBINED_PARAMETER, value=True)
                    self.c.AddSectionorValueToConfig(section=self.card_name, param=PAYMENT_INDEX, value=csv_col)
                    config_params.remove(COMBINED_PARAMETER)
                    config_params.remove(PAYMENT_INDEX)
                else:
                    # write the parameter selected to the config with its associated column name
                    self.c.AddSectionorValueToConfig(section=self.card_name, param=assoc_param, value=csv_col)
                    config_params.remove(assoc_param)
        for cp in config_params:
            self.c.AddSectionorValueToConfig(section=self.card_name, param=cp)
        self.c.AddSectionorValueToConfig(section=self.card_name, param=SETUP_PARAMETER, value=True)
        self.c.AddSectionorValueToConfig(section=self.card_name, param=INCOME_PARAMETER, value=bool(self.AccountFeaturesIncome.get()))
        self.window.destroy()
    
    def Cancel(self):
        print("Cancelling setup!")
        self.c.AddSectionorValueToConfig(section=self.card_name, param=SETUP_PARAMETER, value=False)
        self.window.destroy()