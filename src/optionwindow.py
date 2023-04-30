import tkinter as tk
from config import *
import configparser

class OptionWindow:
    def __init__(self, root, fname, cols, cardname, columnofchoice, desc):
        self.filename = fname
        self.columns = cols
        self.description = desc
        self.columnofchoice = columnofchoice
        self.card_name = cardname
        self.window = tk.Toplevel(root)
        self.window.title("Setup")

        self.TopArea = tk.Frame(self.window)
        self.TopArea.grid(row=0, column=0)
        tk.Label(self.TopArea, text=self.description).grid(row=0, column=0)

        self.BottomArea = tk.Frame(self.window)
        self.BottomArea.grid(row=1, column=0)
        for i,c in enumerate(cols):
            tk.Button(self.BottomArea, text=c, command=lambda:self.WriteToConfig(c)).grid(row=0, column=i)

        self.window.wait_window()

    def WriteToConfig(self, key):
        parameters = configparser.ConfigParser()
        parameters.read(PARAMETER_FILE)
        parameters.set(self.card_name, self.columnofchoice, key)
        with open(PARAMETER_FILE, 'w') as pfile:
            parameters.write(pfile)
