from google.oauth2.service_account import Credentials
from colorama import Fore, init
import gspread


# Initialize Colorama
init()

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


def connect_to_google_sheets():
    """Connect to Google Sheets using service account credentials.
       Returns a Google Sheet instance"""

    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPE_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
    SHEET = GSPREAD_CLIENT.open('salon_lavida_pricelist')
    return SHEET


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

    print(Fore.GREEN + "Welcome to Salon Lavida Service Cart! Let’s\n"
          "make your Salon management easier by tracking sales\n"
          "and sending data directly to Google Sheets.\n")

    print(Fore.BLUE + "Good morning Jo-Ann, let's make some money!\n")

    def get_user_input(self, prompt_message):
        """Get user input with abort functionality"""
        value = input(f"{prompt_message} (Enter 'q' to abort):\n")
        if value.lower() == 'q':
            print(Fore.YELLOW + "Operation aborted.")
            return None
        return value

    def display_menu(self):
        """Create a list of functions."""

        print(Fore.WHITE + "\n===Customer Service Slip===")
        print("1. Add Products")
        print("2. Show selected product list")
        print("3. Remove Product from list")
        print("4. Checkout")
        print("Enter 'q' to quit.\n")

    def show_available_products(self):
        """Display the available products."""

        print("Available products: ")
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
            print(Fore.RED + "Oh no, that product is not in your list,"
                  "please choose another.")

    def add_products(self):
        """Add multiple products."""
        self.show_available_products()
        n_service_to_do = self.get_user_input("\nHow many products do\n"
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
                print(Fore.RED + "Please enter a valid number greater than 0")
                return
        except ValueError:
            print(Fore.RED + "Invalid number. Please try again.")
            return

        for _ in range(n_service_to_do):
            code = self.get_user_input("Enter the product code:\n")
            if code is None:
                break
            self.add_product(code)

        print(self.product_list.service_to_do)

    def show_selected_products(self):
        """Show the products in the dict available for choosing."""

        if not self.product_list.service_to_do:
            print(Fore.RED + "\n No product selected!")
        else:
            print(Fore.GREEN + "\n Selected Products: ")
            for item in self.product_list.service_to_do:
                print(f"- {item['product']}")

    def remove_product(self):
        """Remove Item from chosen list."""

        # Check if a list was entered.
        if not self.product_list.service_to_do:
            print(Fore.RED + "No products in the list to remove.")
            return

        task_to_remove = self.get_user_input("Enter the product name or code\n"
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
            print(Fore.GREEN + "Updated list: ")
            for item in self.product_list.service_to_do:
                print(f" - {item['product']}")
        else:
            print(Fore.RED + "No products left in the list.")

    def checkout(self):
        """Add chosen products to list.

        Send the relevant sales data to Google sheet.
        """

        if not self.product_list.service_to_do:
            print(Fore.RED + "No products to check out.")
        else:

            total_price = self.product_list.total_price
            total_cost = self.product_list.total_cost

            print(Fore.GREEN + "Checkout complete! Saving\n"
                  "sales data to file...")
            print(Fore.BLUE + f"Total Price: ${total_price}")
            print(Fore.RED + f"Total Cost: ${total_cost}")
            print(Fore.GREEN + f"Profit: ${total_price - total_cost}")

            # send the data to google sheets
            sheet = connect_to_google_sheets()
            worksheet = sheet.worksheet('daily_sales')

            for item in self.product_list.service_to_do:
                product_name = item['product']
                product = next((p for p in self.product_list.products
                                if p.name == product_name), None)
                if product:
                    product_price = product.price
                    product_cost = product.cost
                    profit = product_price - product_cost

                    row_data = [product_name, product_price,
                                product_cost, profit]

                    # Send data to google worksheet
                    worksheet.append_row(row_data)
                else:
                    print(f"Error: Product '{product_name}' not found")

            # Reset the list after checkout
            self.product_list.service_to_do.clear()

            print("Product list succesfully closed and ready for more action!")

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
                print("Invalid choice, try again.")


app = ServiceToDoApp()
app.run()
