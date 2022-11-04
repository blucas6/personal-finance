import os

from application import Application
from config import *



def Clean():
    if not os.path.exists(STATEMENT_DIR):
        os.makedirs(STATEMENT_DIR)


##############################################################
############## RUN SEQUENCE ##################################
Clean()
app = Application()
app.geometry("%sx%s"%(WIN_WIDTH, WIN_HEIGHT))
app.mainloop()

##############################################################