# FONTS
LARGE_FONT= ("Verdana", 20)
MEDIUM_FONT = ("Verdana", 14)
SMALL_FONT = ("Verdana", 10)
ITALIC_FONT = ("TkDefaultFont", 12, "italic")
ITALIC_SMALL_FONT = ("TkDefaultFont", 10, "italic")


# WINDOW
WIN_WIDTH = 1650
WIN_HEIGHT = 900


# STATEMENT DIRECTORY
STATEMENT_DIR = "../raw"
CUSTOM_DATA_DIR = "../data"

# PARAMETER FILE
PARAMETER_FILE = "parameters.ini"


# DATA TABLE
CATEGORY_INDEX = 'category'      # column that category is stored in
PAYMENT_INDEX = 'payment'         # column that price is stored in
TRANSACTIONDATE_INDEX = 'date'
DESCRIPTION_INDEX = 'description'
CREDIT_INDEX = 'credit'
CARD_INDEX = 'card_number'
COMBINED_PARAMETER = 'combined'
SETUP_PARAMETER = 'setup'
INCOME_PARAMETER = 'income'

DT_COLUMN_NAMES = [CARD_INDEX, TRANSACTIONDATE_INDEX, DESCRIPTION_INDEX, CATEGORY_INDEX, PAYMENT_INDEX, CREDIT_INDEX]   # represents the names for the config params
DT_DISPLAY_NAMES = ['Category', 'Payment', 'Transaction Date', 'Description', 'Credit', 'Card Number']

# ICONS
ICON_FOLDER = "../icons"
ICON_SIZE = (32,32)
ICON_SIZE_SMALL = (16, 16)
