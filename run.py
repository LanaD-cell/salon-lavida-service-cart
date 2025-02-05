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

# serializing date

my_dateJSONData = json.dumps(my_date, cls=DateTimeEncoder)
print(my_dateJSONData)

#add to google worksheet
SHEET = connect_to_google_sheets()
daily_cost_worksheet = SHEET.worksheet("daily_cost")
daily_profit_worksheet = SHEET.worksheet("daily_profit")

#add to row

daily_cost_worksheet.append_row([my_date_str])
daily_profit_worksheet.append_row([my_date_str])
print("Date added to worksheet\n")

print("Please enter the clients name: \n")
clients_name = input()

def get_prices(SHEET):
    """
    pull the item pricing from the google sheet
    """
    price_list_worksheet = SHEET.worksheet("price_list")
    items_and_prices = price_list_worksheet.get_all_records()
    return{row['item']: row['price'] for row in items_and_prices}


def display_cart(service_cart):
    """
    creating a basic shopping cart - I followed along with this video 
    'Python Mini Project for Beginners | Build a Simple Python Shopping Cart App using LISTS'
    """
    if not service_cart:
        print("Service cart is still empty")
    else:
        print("Service cart: \n")    
    total_price = 0
    for item in service_cart:
        print(f"{item['name']}:${item['price']}")
        total_price += item['price']
    print(f"Total: ${total_price:}")

def main():
    prices = get_prices(SHEET)
    total_prices = [] # file to store total price of each cart at end

    while True:
        service_cart = [] # file to reset cart
        total_price = 0

        print("Service cart App")
        print("1. 20 Volume Oxide")
        print("2. 30 Volume Oxide ")
        print("3. Be Blond Lifting Powder")
        print("4. Time")
        print("5. Blowdry")
        print("6. Checkout")
        print("Enter 'q' to quit.\n")

        choose = input ("Choose your products used (Products are in Portion quantities) or press 'q' to quit: \n")
        if choose.lower() == 'q':
            total_prices.append(total_price)
            print(f"Total earnings so far: {total_prices}\n")
            break

        item_map = {
            "1": "20 Volume Oxide",
            "2": "30 Volume Oxide",
            "3": "Be Blond Lifting Powder",
            "4": "Time",
            "5": "Blowdry"
        }

        if choose in item_map:
            name = item_map[choose]
            price = prices.get(name, "Price not available")
            print(f"{name} costs ${price}\n")
            service_cart.append({'name':name, 'price':price})
            total_price += price
        else:
            print("Invalid Item chosen, please try again.")    

        display_cart(service_cart)

    print("Total Price and cost for service provided:", service_cart)    

if __name__ == "__main__":
    main()
