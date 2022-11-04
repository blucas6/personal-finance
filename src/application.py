import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
import os

from config import *
from homepage import Homepage
from sessionpage import Sessionpage

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.app_container = tk.Frame(self)
        self.app_container.pack(side="top", fill="both", expand=True)
        self.app_container.grid_rowconfigure(0, weight=1)
        self.app_container.grid_columnconfigure(0, weight=1)

        #################### MAIN VARIABLES ##########################
        self.transaction_header = []
        self.all_transactions = []
        ##############################################################

        ################ MENU BAR ####################################
        self.menubar = tk.Menu(self.app_container)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Import Data", command=lambda:self.ImportData())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        tk.Tk.config(self, menu=self.menubar)
        ##############################################################

        self.app_frames = {}
        for F in (Sessionpage, Homepage):
            frame = F(self.app_container, self)
            self.app_frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.ShowFrame(Homepage)

    def ShowFrame(self, cont):
        f = self.app_frames[cont]
        f.tkraise()

    def ImportData(self):
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files","*.txt*"),("all files","*.*")))
        shutil.copy(filename, STATEMENT_DIR)
