from google.oauth2.service_account import Credentials
"""
Connects to google spreadsheets
"""
import gspread
import colorama
"""
Use Colorama to bring color to my code
"""
from colorama import Fore, init


# Initialize Colorama
init()

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


def connect_to_google_sheets():
    """
    Define scope, this feature was initially planned to send
    sales data to google sheets
    """

    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPE_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
    sheet = GSPREAD_CLIENT.open('salon_lavida_pricelist')
    return sheet


class ServiceToDoApp:
    """
    Create a class to ensure the app can be used repeatedly
    """
    def __init__ (self):
        self.total_price = 0
        self.total_cost = 0

        # Read: https://www.w3schools.com/python/python_functions.asp
        # Create a product dict with price and cost.
        self.products_dict = {
            '001': {'name': '20 Volume Oxide', 'price': 55, 'cost': 15},
            '002': {'name': '30 Volume Oxide', 'price': 65, 'cost': 25},
            '003': {'name': 'Be Blond Lifting Powder',
                    'price': 35, 'cost': 17},
            '004': {'name': 'Blowdry', 'price': 44, 'cost': 0},
            '005': {'name': 'Time', 'price': 65, 'cost': 0}
        }
        # Create list to hold the products chosen
        self.service_to_do = []
    print(Fore.GREEN + "Welcome to Salon Lavida Service Cart! Let’s"
          "make your Salon management easier by tracking sales"
          "and sending data directly to Google Sheets.\n")

    print(Fore.BLUE + "Good morning Jo-Ann, let's make some money!\n")

    def display_menu(self):
        """
        Create a list of functions for the user to navigate the menu
        """
        print(Fore.WHITE + "\n===Customer Service Slip===")
        print("1. Add Products")
        print("2. Show selected product list")
        print("3. Remove Product from list")
        print("4. Checkout")
        print("Enter 'q' to quit.\n")

    def show_available_products(self):
        """
        Show the products that can be chosen, with product info
        when "1" is pressed
        """
        print("Available products: ")

        for code, details in self.products_dict.items():
            print(f"{code}. {details['name']} - Price:${details['price']} - "
                  f"Cost:${details['cost']}")

    def add_product(self, code):
        """
        Add product to list
        """
        if code in self.products_dict:
            product = self.products_dict[code]
            item = {"product": product['name'], "done": False}
            self.service_to_do.append(item)

            # Update totals
            self.total_price += product['price']
            self.total_cost += product['cost']

            print(f"Product '{product['name']}' added!")
            print(f"Total Price:${self.total_price} | "
                  f"Total Cost: ${self.total_cost}")
        else:
            print(Fore.RED + "Oh no that Product is not in your list,"
                  "please choose another")

    def add_products(self):
        """
        Add multiple products
        """
        self.show_available_products()
        n_service_to_do = int(input
                              ("\nHow many products do you want to add? "))
        for _ in range(n_service_to_do):
            code = input("Enter the product code: ")
            if code in self.products_dict:
                self.add_product(code)
            else:
                print(Fore.RED + "Product code not found, try again.")
        print(self.service_to_do)

    def show_selected_products(self):
        """
        Show the products in the dict available for choosing
        """
        if not self.service_to_do:
            print(Fore.RED + "\n No product selected!")
        else:
            print(Fore.GREEN + "\n Selected Products: ")
            for item in self.service_to_do:
                print(f"- {item['product']}")

    def remove_product(self):
        """
        Remove Item from chosen list
        """
        task_to_remove = input("Enter the product to be removed: ")
        # Check if the product was found
        product_found = False

        # Create a list for the removed item to be kept
        item_to_remove = None

        for item in self.service_to_do:
            # Find the product that matches the ite, to be removed
            product_name = item['product']
            product_code = next((code for code, details in
                                self.products_dict.items()
                                if details['name'] == product_name), None)

            if product_code == task_to_remove:
                # remove the cost and price of item from the list
                self.total_price -= self.products_dict[product_code]['price']
                self.total_cost -= self.products_dict[product_code]['cost']

                item_to_remove = item
                # Check that the product was found
                product_found = True
                break

        if item_to_remove:
            self.service_to_do.remove(item_to_remove)
            print(f"product with code {task_to_remove} removed from the list.")
        else:
            print(f"Product code '{task_to_remove}' not found in the list.")

        self.show_selected_products()

    def checkout(self):
        """ Add chosen products to list and send cost
        and price to daily_sales.txt
        """
        if not self.service_to_do:
            print(Fore.RED + "No products to check out.")
        else:

            total_price = self.total_price
            total_cost = self.total_cost

            print(Fore.GREEN + "Checkout complete! Saving"
                  "sales data to file...")
            print(Fore.BLUE + f"Total Price: ${total_price}")
            print(Fore.RED + f"Total Cost: ${total_cost}")
            print(Fore.GREEN + f"Profit: ${total_price - total_cost}")

            # send the data to google sheets
            sheet = connect_to_google_sheets()
            worksheet = sheet.worksheet('daily_sales')

            for item in self.service_to_do:
                product_name = item['product']
                product_code = next((code for code,
                                    details in self.products_dict.items()
                                    if details['name'] == product_name),
                                    None)

                if product_code:
                    product_price = self.products_dict[product_code]['price']
                    product_cost = self.products_dict[product_code]['cost']
                    profit = product_price - product_cost

                    row_data = [product_name, product_price,
                                product_cost, profit]

                    # Send data to google worksheet
                    worksheet.append_row(row_data)
                else:
                    print(f"Error: Product code for "
                          f"'{product_name}' not found")

            # Reset the list after checkout
            self.service_to_do.clear()
            self.total_cost = 0
            self.total_price = 0
            print("Product list succesfully closed and ready for more action!")

    def calculate_totals(self):
        """
        Calculate totals for each list created
        """
        total_price = 0
        total_cost = 0
        for item in self.service_to_do:
            product_name = item['product']
            product_code = next((code for code,
                                 details in self.products_dict.items()
                                 if details['name'] == product_name), None)

            if product_code:
                self.total_price += self.products_dict[product_code]['price']
                self.total_cost += self.products_dict[product_code]['cost']

        return total_price, total_cost

    def run(self):
        """
        Calling the relevent functions associated with the options presented
        """
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_products()
            elif choice == '2':
                self.show_selected_products()
            elif choice == '3':
                self.remove_product()
            elif choice == '4':
                self.checkout()
            elif choice.lower() == 'q':
                break   # break the while loop
            else:
                print("Invalid product choice, try again.")


app = ServiceToDoApp()
app.run()
