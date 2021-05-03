# flask-eshop
An imaginary e-shop.

# Instructions to run the app
- Create an virtual env
- pip install -r requirements.txt
- type flask run in bash
- Go to http://127.0.0.1:5000/ and add a date in a format of dd-mm-yyyy


# The checklist of the task
- The total number of items sold on that day. Check
- The total number of customers that made an order that day. Check
- The total amount of discount given that day. check
- The average discount rate applied to the items sold that day. check
- The average order total for that day. check
- The total amount of commissions generated that day. check
- The average amount of commissions per order for that day. check
- The total amount of commissions earned per promotion that day. check


# Strategy of the commissions part
- Create a list with the order_id of each vendor
- Add the total amount of each order with the same vendor
- Get the the rate for the specific date 
- Multiply the rate with the total amount to find the commission
- Connect vendors with order
