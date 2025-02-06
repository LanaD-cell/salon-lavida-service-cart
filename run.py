import gspread 
from google.oauth2.service_account import Credentials

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

class ServiceToDoApp:
        # read for some more clarity :https://micropyramid.com/blog/understand-self-and-__init__-method-in-python-class#:~:text=self%20represents%20the%20instance%20of,of%20the%20class%20in%20python.&text=%22__init__%22%20is%20a%20reseved,constructor%20in%20object%20oriented%20concepts.
    def __init__ (self):  
        
        # Create a product dict with price and cost    
        self.products_dict = {
            '001': {'name': '20 Volume Oxide', 'price': 55, 'cost': 15}, 
            '002': {'name': '30 Volume Oxide', 'price': 65, 'cost': 25}, 
            '003': {'name': 'Be Blond Lifting Powder', 'price': 35, 'cost': 17}, 
            '004': {'name': 'Blowdry', 'price': 44, 'cost': 0}, 
            '005': {'name': 'Time', 'price': 65, 'cost': 0}
        }
        
        self.service_to_do = []  #create list to hold the products chosen

        print("Good morning Jo-Ann, let's make some money!\n")

    def display_menu(self):
        # Create a list of functions for the user to navigate the menu
        print("\n===Service To-Do App===")
        print("1. Add Products")
        print("2. Show selected product list")
        print("3. Remove Product from list")
        print("4. Checkout")
        print("Enter 'q' to quit.\n")

    def add_products(self):
        # Show available products
        print("Avavilable products: ")
        product_codes = {str(index +1): product for index, product in enumerate(self.products_dict.keys())}

        for code, product in product_codes.items():
            price = self.products_dict[product][0]
            print(f"{code}. {product} - price: ${price}")

        #  Add product to the list and append
        n_service_to_do = int(input("How many products do you want to add: "))
            
        for i in range(n_service_to_do):
            code = input("Enter the product code to add to the list: ")
            if code in product_codes:
                task = product_codes[code]
                self.service_to_do.append({"products": task, "done": False})
                print("Product added!")
            else:
                print("Oh no that Product is not in your list, choose another")    

    def show_selected_products(self):
        # Show the products in the dict available for choosing
        if not self.service_to_do:
            print("\n No product selected!")
        else:
            print(f"\n Selected Products: ")
            for item in self.service_to_do:
                print(f"- {item['product']}")
  
    def remove_product(self):
        # Remove Item from chosen list
        task_to_remove = input("Enter the product to be removed: ")
        self.service_to_do = [item for item in self.service_to_do if item["product"] != task_to_remove]
        print(f"{task_to_remove} removed from the list.")

    def checkout(self):
        # Add chosen products to list and send cost and price to daily_sales.txt
        if not self.service_to_do:
            print("No products to check out.")
        else:
            print("Checkout complete! Saving sales data to file...")

            # Write the data to the txt file
            with open("daily_sale.txt", "a") as file:  # read about this method in: https://stackoverflow.com/questions/29956883/appending-data-to-txt-file
                for item in self.service_to_do:
                    product_name = item['product']
                    product_price = self.products_dict[product_name][0]
                    product_cost = self.products_dict[product_name][1] 
                    file.write(f"{product_name} - ${product_price}\n")
     
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