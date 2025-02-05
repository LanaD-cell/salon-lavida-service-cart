import gspread  
from google.oauth2.service_account import Credentials
import json
from json import JSONEncoder
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

# create a date generator - (stackoverflow solution)
my_date = {'date': datetime.datetime.now()} 

#convert date to string
my_date_str = my_date['date'].strftime('%Y-%m-%d %H:%M:%S') 

class DateTimeEncoder(JSONEncoder):
    """
    create a date that is serializable to 
    send to my worksheets, 
    'https://pynative.com/python-serialize-datetime-into-json/'
    """
    def default(self, obj):
        if isinstance(obj, (datetime.date)):
            return obj.isoformat()

#serializing date
my_dateJSONData = json.dumps(my_date, cls=DateTimeEncoder)

print(my_dateJSONData)

#add to google worksheet
daily_cost_worksheet = SHEET.worksheet("daily_cost")
daily_profit_worksheet = SHEET.worksheet("daily_profit")
#add to row
daily_cost_worksheet.append_row([my_date_str])
daily_profit_worksheet.append_row([my_date_str])
print("Date added to worksheet\n")

print("Please enter the clients name:")
clients_name = input()
    
