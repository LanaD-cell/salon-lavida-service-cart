import gspread  
from google.oauth2.service_account import Credentials
import json
import datetime

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

# add datetime for service cart (W3Schools)
print("Todays date is: ")
date = datetime.datetime.now()

# Convert the datetime object to a string in a specific format 
date_str = date.strftime("%Y-%m-%d %H:%M:%S") 

"""
Serialize the object using the custom function 
(error when running to worksheet - geeksforgeeks)
"""
json_data = json.dumps(date_str) 

print(json_data) 

# add to google worksheet
daily_cost_worksheet = SHEET.worksheet("daily_cost")
daily_cost_worksheet.append_row("Date")
print("Date added to worksheet")

date = datetime.datetime.now()
