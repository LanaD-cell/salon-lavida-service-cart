

Welcome,

**Introduction to Salon LaVida Service Management System**

Welcome to the Service Management System for Salon LaVida, a dynamic and user-friendly Python project designed specifically to streamline the process of managing services, pricing, and sales for the salon. Inspired by the needs of my sister's salon, this project integrates essential business functions, allowing the salon to maintain accurate and organized records of the products and services used throughout the day.

The core functionality of the system includes adding, removing, and tracking products and services, calculating totals, and handling sales data efficiently.

### Key Features:
- **Product Management**: The system stores a list of products and their corresponding prices and costs, from hair care treatments to styling products. Each product can be added or                        removed as services are completed.
- **Service List Management**: Salon employees can add and remove services to a customer’s order list, displaying the total price and cost in real-time.
- **Checkout Process**: Once services are complete, the system calculates the total price, cost, and profit, and saves the sales data to a `daily_sales.txt` file for record-keeping.


By implementing this system, Salon LaVida ensures accurate pricing and
inventory tracking, while also optimizing the overall customer experience
by reducing administrative overhead.

Let’s make the business process smoother, organized, and more profitable
with this tool!

 **February 10, 2025**

## Functionality

<img src="./assets/initial_page.png">

- Initial page featuring a welcome message and a list of functions to choose from.

<img src="./assets/function_menu.png">

- The list of functions to choose from and a prompt for the user to enter the chosen option.

<img src="./assets/product_menu.png">

- When a option "1" is chosen, the product menu is shown, with a prompt to the user to
confirm the number of items that should be added to the list.

<img src="./assets/choose_total_menu_items_to_add.png">

- The list only contains 5 Items for this project, but the list can be
added to in the future and adjusted as products change.

<img src="./assets/enter_product_codes_to_add.png">

- A prompt for the user to enter the relevant item codes.

<img src="./assets/list_items_added.png">

- A list of the Items added to the list is displayed.
- In the instance a irrelevant code is entered a "false" statement will appear for only that code.

<img src="./assets/checkout_after_service_completed.png">

- Once the list/service is completed the checkout function can be triggered by choosing option "4".

<img src="./assets/total_cos_total_price_basket_reset.png">

- Upon successful checkout the total price and cost will be shown and relevent sales data will be sent to Daily_sales.txt.

<img src="./assets/q_for_quit.png">

- "q" can be used at any step in the process to abort.

<img src="./assets/data_sent_to_daily_sales_txt.png">

- The data is then added to the daily_sales.txt file.

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
