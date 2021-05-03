from app import db
from flask import Flask
from csv import reader
from app.models import Order, OrderLine, Products, Promotion, \
                       ProductPromotion, VendorCommissions
from datetime import datetime


app = Flask(__name__)


def populate():
    """
    The method run when environment is set to populate.
    Iterate through the .csv files and getting every row of every file
    and populate the database.
    """
    if __name__ == "app.populate_db":
        try:
            file_list = ['orders', 'order_lines', 'products', 'promotions', 'product_promotions', 'commissions']
            for file_name in file_list:
                    
                file = open('app/csv_data/' + file_name +'.csv', encoding='utf8')
                data = reader(file, delimiter=',') 
                next(data)

                for entry in data:
                    if file_name == 'orders':
                        row = Order (
                            id = entry[0],
                            created_at = datetime.strptime(entry[1], '%d/%m/%Y').date(),
                            vendor_id = entry[2],
                            customer_id = entry[3]
                        )
                    if file_name == 'order_lines':
                        row = OrderLine (
                            order_id = entry[0],
                            product_id = entry[1],
                            product_description = entry[2],
                            product_price = entry[3],
                            product_vat_rate = entry[4],
                            discount_rate = entry[5],
                            quantity = entry[6],
                            full_price_amount = entry[7],
                            discounted_amount = entry[8],
                            vat_amount = entry[8],
                            total_amount = entry[8]
                        )
                    if file_name == 'products':
                        row = Products (
                            id = entry[0],
                            description = entry[1]
                        )
                    if file_name == 'promotions':
                        row = Promotion (
                            id = entry[0],
                            description = entry[1]
                        )
                    if file_name == 'product_promotions':
                        row = ProductPromotion (
                            date = datetime.strptime(entry[0], '%d/%m/%Y').date(),
                            product_id = entry[1],
                            promotion_id = entry[2]
                        )
                    if file_name == 'commissions':
                        row = VendorCommissions (
                            date = datetime.strptime(entry[0], '%d/%m/%Y').date(),
                            vendor_id = entry[1],
                            rate = entry[2]
                        )
                    
                    db.session.add(row)

            db.session.commit()
            print('Finished')
        except Exception as error:
            print(error) 
