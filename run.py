from datetime import datetime
from google.oauth2.service_account import Credentials
from colorama import Fore, Style, init
import gspread
import pyfiglet as pf

textArt = pf.figlet_format("SALON LAVIDA", font="bubble")
print(textArt)

now = datetime.now()

# Initialize Colorama
init()

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


def connect_to_google_sheets():
    """Connect to Google Sheets using service account credentials.
       Returns a Google Sheet instance"""

    creds = Credentials.from_service_account_file('creds.json')
    scope_creds = creds.with_scopes(scope)
    gspread_client = gspread.authorize(scope_creds)
    sheet = gspread_client.open('salon_lavida_pricelist')
    return sheet


class Product:
    """Class to represent the products."""

    def __init__(self, code, name, price, cost):
        self.code = code
        self.name = name
        self.price = price
        self.cost = cost


class ProductList:
    """Class to manage the product catalog."""

    def __init__(self):
        self.total_price = 0
        self.total_cost = 0
        self.products = [
            Product('001', '20 Volume Oxide', 55, 15),
            Product('002', '30 Volume Oxide', 65, 25),
            Product('003', 'Be Blond Lifting Powder', 35, 17),
            Product('004', 'Blowdry', 44, 0),
            Product('005', 'Time', 65, 0)
        ]

        # Create list to hold the products chosen
        self.service_to_do = []
        self.total_cost = 0
        self.total_price = 0


class ServiceToDoApp:
    """Create a class to ensure the app can be used repeatedly"""
    def __init__(self):
        self.product_list = ProductList()

    def checkout(self):
        """Handle checkout and send sales data to Google Sheets."""

        if not self.product_list.service_to_do:
            print(Fore.RED + "No products to check out.")
            return

        total_price = self.product_list.total_price
        total_cost = self.product_list.total_cost

        print(Fore.WHITE + "Checkout complete! Saving sales to Gspread...")
        print(Style.BRIGHT + Fore.BLUE + f"Total Price: ${total_price}")
        print(Style.BRIGHT + Fore.RED + f"Total Cost: ${total_cost}")
        print(Style.BRIGHT + Fore.GREEN + f"Profit:"
              f"${total_price - total_cost}")

        # Connect to Google Sheets
        sheet = connect_to_google_sheets()
        worksheet = sheet.worksheet('daily_sales')

        rows_to_add = []

        # Collect product data for Google Sheets
        for item in self.product_list.service_to_do:
            product_name = item['product']
            product = next((p for p in self.product_list.products if
                            p.name == product_name), None)
            if product:
                product_price = product.price
                product_cost = product.cost
                profit = product_price - product_cost
                date = now.strftime("%d-%m-%Y")

                row_data = [date, product_name, product_price,
                            product_cost, profit]
                rows_to_add.append(row_data)

        # Append rows only once
        if rows_to_add:
            worksheet.append_rows(rows_to_add)
            print(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + "Data successfully\n"
                  "saved to Google Sheets.")
        else:
            print(Style.BRIGHT + Fore.RED + "No data to save.")

        # Clear product list and reset totals after checkout
        self.product_list.service_to_do.clear()
        self.product_list.total_price = 0
        self.product_list.total_cost = 0

        print(Fore.WHITE + "Product list successfully\n"
              "cleared and totals reset.")

    print(Style.BRIGHT + Fore.LIGHTBLUE_EX + "Service Cart!\n"
          "Let’s make your Salon management easier\n"
          "by tracking sales and sending data directly\n"
          "to Google Sheets.\n"
          "Choose the relevant number corresponding\n"
          "to the funtion required.\n")

    textArt = pf.figlet_format("HELLO JO-ANN", font="bubble")
    print(textArt)

    print(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + "Let's make some money!\n")

    print(Fore.WHITE + "Date is (DD-MM-YYYY format): ",
          now.strftime("%d-%m-%Y"))

    def get_user_input(self, prompt_message):
        """Get user input with abort functionality"""
        value = input(f"{prompt_message} (Enter 'q' to abort):\n")
        if value.lower() == 'q':
            print(Style.BRIGHT + Fore.YELLOW + "Operation aborted.")
            return None
        return value

    def display_menu(self):
        """Create a list of functions."""

        print(Fore.WHITE + "\n===Customer Service Slip===")
        print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "1. Add Products")
        print(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + "2. Show selected\n"
              "product list")
        print(Style.BRIGHT + Fore.LIGHTRED_EX + "3. Remove Product from list")
        print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "4. Checkout")
        print(Style.BRIGHT + Fore.CYAN + "Enter 'q' to quit.\n")

    def show_available_products(self):
        """Display the available products."""

        print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Available products: ")
        for product in self.product_list.products:
            print(f"{product.code}. {product.name} - Price:${product.price}"
                  f" - Cost:${product.cost}")

    def get_product_by_code(self, code):
        """Find a product by its code."""
        for product in self.product_list.products:
            if product.code == code:
                return product
        return None

    def add_product(self, code):
        """Add product to list."""
        product = self.get_product_by_code(code)
        if product:
            item = {"product": product.name, "done": False}
            self.product_list.service_to_do.append(item)
            self.product_list.total_price += product.price
            self.product_list.total_cost += product.cost

            print(f"Product '{product.name}' added!")
            print(f"Total Price:${self.product_list.total_price} | "
                  f"Total Cost: ${self.product_list.total_cost}")
        else:
            print(Style.BRIGHT + Fore.RED + "Oh no, that product\n"
                  "is not in your list, please choose another.")

    def add_products(self):
        """Add multiple products."""
        self.show_available_products()
        n_service_to_do = self.get_user_input(Fore.WHITE +
                                              "\nHow many products do\n"
                                              "you want to add?\n ")

        # Check for q (abort)
        if n_service_to_do is None:
            return

        # Allow user to abort at this point by entering 'q'
        if n_service_to_do.lower() == 'q':
            print(Fore.YELLOW + "Operation aborted.")
            return

        try:
            n_service_to_do = int(n_service_to_do)
            if n_service_to_do <= 0:
                print(Style.BRIGHT + Fore.RED + "Please enter a\n"
                      "valid number greater than 0")
                return
        except ValueError:
            print(Style.BRIGHT + Fore.RED + "Invalid number.\n"
                  "Please try again.")
            return

        for _ in range(n_service_to_do):
            code = self.get_user_input(Style.BRIGHT + Fore.LIGHTMAGENTA_EX +
                                       "Enter the product code:\n")
            if code is None:
                break
            self.add_product(code)

    def show_selected_products(self):
        """Show the products in the dict available for choosing."""

        if not self.product_list.service_to_do:
            print(Style.BRIGHT + Fore.RED + "\n No product selected!")
        else:
            print(Style.BRIGHT + Fore.GREEN + "\n Selected Products: ")
            for item in self.product_list.service_to_do:
                print(f"- {item['product']}")

    def remove_product(self):
        """Remove Item from chosen list."""

        # Check if a list was entered.
        if not self.product_list.service_to_do:
            print(Style.BRIGHT + Fore.RED + "No products\n"
                  "in the list to remove.")
            return

        task_to_remove = self.get_user_input(Fore.WHITE +
                                             "Enter the product name or code\n"
                                             "to be removed:\n")

        if task_to_remove is None:
            return

        # Find the item in the service list
        item_to_remove = next(
            (item for item in self.product_list.service_to_do
             if item['product'] == task_to_remove
             or any(p.code == task_to_remove and p.name == item['product']
                    for p in self.product_list.products)), None)

        if item_to_remove:
            product_name = item_to_remove['product']
            product = next((p for p in self.product_list.products if p.name
                            == product_name), None)

            if product:
                self.product_list.total_price -= product.price
                self.product_list.total_cost -= product.cost

            self.product_list.service_to_do.remove(item_to_remove)
            print(f"Product '{product_name}' removed from the list.")
        else:
            print(f"Product '{task_to_remove}' not found in the list.")

        # Display updated list after removing product.
        if self.product_list.service_to_do:
            print(Style.BRIGHT + Fore.GREEN + "Updated list: ")
            for item in self.product_list.service_to_do:
                print(f" - {item['product']}")
        else:
            print(Style.BRIGHT + Fore.RED + "No products left in the list.")

    def calculate_totals(self):
        """Calculate totals for each list created."""

        total_price = 0
        total_cost = 0

        for item in self.product_list.service_to_do:
            product_name = item['product']
            product = next((p for p in self.product_list.products
                            if p.name == product_name), None)

            if product:
                total_price += product.price
                total_cost += product.cost

        return total_price, total_cost

    def run(self):
        """Call the relevent functions."""

        while True:
            self.display_menu()
            choice = input(Fore.WHITE + "Enter your choice: ")
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
                print(Style.BRIGHT + Fore.RED + "Invalid choice, try again.")


app = ServiceToDoApp()
app.run()
