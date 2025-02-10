import gspread
""" Connects to google spreadsheets"""
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


def connect_to_google_sheets():
    """
    Define scope, this feature was initially planned to send
    sales data to google sheets
    """

    creds = Credentials.from_service_account_file('creds.json')
    scope_creds = creds.with_scopes(scope)
    gspread_client = gspread.authorize(scope_creds)
    sheet = gspread_client.open('salon_lavida_pricelist')
    return sheet


class ServiceToDoApp:
    """
    Read for some more clarity :https://micropyramid.com/blog/understand-
    self-and-__init__-method-in-python-class#:~:text=self%20
    represents%20the%20instance%20of,of%20the%20class%20in%20python.
    &text=%22__init__%22%20is%20a%20reseved,
    constructor%20in%20object%20oriented%20concepts.
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
       
    print("Good morning Jo-Ann, let's make some money!\n")

    def display_menu(self):
        # Create a list of functions for the user to navigate the menu
        print("\n===Customer Service Slip===")
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
        # Add product to list
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
            print("Oh no that Product is not in your list, choose another")  

    def add_products(self):
        # Add multiple products 
        self.show_available_products()
        n_service_to_do = int(input
                              ("\nHow many products do you want to add? "))
        for i in range(n_service_to_do):
            code = input("Enter the product code: ")
            if code in self.products_dict:
                self.add_product(code)  
            else:
                print("Product code not found, try again.")
        print(self.service_to_do)

    def show_selected_products(self):
        # Show the products in the dict available for choosing
        if not self.service_to_do:
            print("\n No product selected!")
        else:
            print("\n Selected Products: ")
            for item in self.service_to_do:
                print(f"- {item['product']}")

    def remove_product(self):
        # Remove Item from chosen list
        task_to_remove = input("Enter the product to be removed: ")
        for item in self.service_to_do:
            if item["product"] == task_to_remove:
                product_name = item['product']
                product_code = next((code for code, details in 
                                     self.products_dict.items() 
                                     if details['name'] == product_name), None)

                if product_code:
                    self.total_price -= self.products_dict
                    [product_code]['price']
                    
                    self.total_cost -= self.products_dict[product_code]['cost']
                self.service_to_do.remove(item)    
                print(f"{task_to_remove} removed from the list.")
                break
        self.show_selected_products()

    def checkout(self):
        """ Add chosen products to list and send cost 
        and price to daily_sales.txt
        """
        if not self.service_to_do:
            print("No products to check out.")
        else:
            """ Calculate the total price and cost when 
            checking out and display on screen
            """
            total_price = self.total_price
            total_cost = self.total_cost

            print("Checkout complete! Saving sales data to file...")
            print(f"Total Price: ${total_price}")
            print(f"Total Cost: ${total_cost}")
            print(f"Profit: ${total_price - total_cost}")

            """
            Write the data to the txt file
            Read about this method in: 
            https://stackoverflow.com/questions/29956883/appending-data-to-txt-file, 
            https://www.youtube.com/watch?v=Dw85RIvQlc8
            """
            with open("daily_sale.txt", "a") as file:  
                for item in self.service_to_do:
                    product_name = item['product']
                    product_code = next((code for code, 
                                        details in self.products_dict.items()
                                        if details['name'] == product_name),
                                        None)

                    if product_code:
                        product_price = self.products_dict[product_code]
                        ['price']
                        product_cost = self.products_dict[product_code]
                        ['cost']
                        file.write(f"{product_name} - ${product_price}"
                                   f"(Cost: ${product_cost})\n")
                    else:
                        print(f"Error: Product code for "
                              f"'{product_name}' not found")
                        
            # Reset the list after checkout
            self.service_to_do.clear()

            self.total_cost = 0
            self.total_price = 0            
            print("Product list succesfully closed and ready for more action!")
    
    def calculate_totals(self):
        # Calculate totals for each list created
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
                print("Invalid product choice, try apain.")


app = ServiceToDoApp()
app.run()