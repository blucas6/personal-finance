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
INCOME_INDEX = 'income'
CARD_INDEX = 'card_number'
COMBINED_PARAMETER = 'combined'
SETUP_PARAMETER = 'setup'

DT_COLUMN_NAMES = [CATEGORY_INDEX, PAYMENT_INDEX, TRANSACTIONDATE_INDEX, DESCRIPTION_INDEX, INCOME_INDEX, CARD_INDEX]
DT_DISPLAY_NAMES = ['Category', 'Payment', 'Transaction Date', 'Description', 'Income', 'Card Number']

# ICONS
ICON_FOLDER = "../icons"
ICON_SIZE = (32,32)
ICON_SIZE_SMALL = (16, 16)
