import gspread  
from google.oauth2.service_account import Credentials
from datetime import date

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('salon_lavida_pricelist')

# welcome
print("Good morning Jo-Ann, lets make some money!\n")


# create input for date (ref Dimitri Patarroyo)
dates = []
DATE = str(input("Please enter the date here (YYYY-MM-DD): "))
daily_date_picker = date.fromisoformat(DATE)

print(daily_date_picker)

# open cart with date

# input cart Name 

# choose relevent products to add to cart

# calculate total price

# calculate total cost and append daily_cost

# calculate profit and append daily_profit

# reset cart for next purchase



