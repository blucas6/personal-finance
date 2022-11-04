import tkinter as tk

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

        self.app_frames = {}
        for F in (Sessionpage, Homepage):
            frame = F(self.app_container, self)
            self.app_frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(Homepage)

    def showFrame(self, cont):
        f = self.app_frames[cont]
        f.tkraise()


app = Application()
app.geometry("%sx%s"%(WIN_WIDTH, WIN_HEIGHT))
app.mainloop()
