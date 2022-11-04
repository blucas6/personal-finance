import tkinter as tk
from tkinter import ttk

from config import *


class Sessionpage(tk.Frame):
    def __init__(self, parent, controller):
        self.c = controller
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Session", font=LARGE_FONT).grid(row=0,column=0)
        ttk.Button(self, text="Start New Session").grid(row=1,column=0)    