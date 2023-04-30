'''
MAIN script: Starting point for running the software
'''
import os

from controller import Controller
from config import *


def Clean():
    if not os.path.exists(CUSTOM_DATA_DIR):
        os.makedirs(CUSTOM_DATA_DIR)
    if not os.path.exists(STATEMENT_DIR):
        os.makedirs(STATEMENT_DIR)
    if not os.path.exists(PARAMETER_FILE):
        fo = open(PARAMETER_FILE, "w+")
        fo.close()


##############################################################
############## RUN SEQUENCE ##################################
Clean()
app = Controller()
app.root.mainloop()
app.root.destroy()
##############################################################