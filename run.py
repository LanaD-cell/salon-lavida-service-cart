import gspread  
from google.oauth2.service_account import Credentials
import json
from json import JSONEncoder
import datetime

def connect_to_google_sheets():
    # define scope
    SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"
            ]

    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPE_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
    SHEET = GSPREAD_CLIENT.open('salon_lavida_pricelist')
    return SHEET

def main():
    service_to_do = [] # create a file to place the chosen items
    """
    Create a product dictionary with pricing and cost to draw data from for the to-do list
    """
    products_dict = {'20 Volume Oxide': (55, 15), 
        '30 Volume Oxide':(65, 25), 
        'Be Blond Lifting Powder': (35, 17), 
        'Blowdry': (44, 0), 
        'Time': (65, 0)
        }
  
    while True:
        print("\n===Service To-Do App===")
        print("1. Add Products")
        print("2. Show selected product list")
        print("3. Remove Product from list")
        print("3. Checkout")
        print("Enter 'q' to quit.\n")

        choice = ("Enter your choice: ")
        if choice == '1'
            print()
            n_service_to_do = int(input("How may task you want to add: "))
            
            for i in range(n_service_to_do):
                task = input("Enter the product: ")
                service_to_do.append({"products": service_to_do, "done": False})
                print("Task added!")

        if choose.lower() == 'q':
            break


     