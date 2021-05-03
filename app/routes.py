from app import app, db
from csv import reader
from app.models import Order, OrderLine, Products, Promotion, \
                       ProductPromotion, VendorCommissions
from datetime import datetime
import os
from flask import send_from_directory
from collections import defaultdict
from flask import jsonify

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/<date>', methods=['GET'])
def metrics(date):
    """
    This endpoint gets a date as a parameter from the url
    and returns the required metrics 
    """
    convert_date = datetime.strptime(date, "%d-%m-%Y")
    total_products_sold = 0
    total_discount_of_the_day = 0
    customers_list = []
    discount_rate_total = 0
    total_number_of_orders = 0
    total_discount_rate = 0
    total_amount = 0 
    sum_amount = 0
    promosion_amount = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }
    
    orders = Order.query\
        .join(OrderLine, Order.id==OrderLine.order_id)\
            .add_columns(OrderLine.quantity, OrderLine.discounted_amount, OrderLine.discount_rate, OrderLine.total_amount, OrderLine.product_id)\
                .filter(Order.created_at==convert_date).all()
      
    promotion_dict = total_amount_per_promotion(convert_date)

    comissions_tuple = total_and_avg_of_commission(convert_date)
    total_commissions_of_the_day = comissions_tuple[0]
    avg_commissions_of_the_day = comissions_tuple[1]

    for order in orders:
        total_number_of_orders += 1
        customers_list.append(order.Order.customer_id)
        total_products_sold += order[1]
        total_discount_of_the_day += order[2]
        total_discount_rate += order[3]
        total_amount += order[4]

        for key, products in promotion_dict.items():
            if order[5] in products:
                if key in promosion_amount.keys():
                    temp = promosion_amount[key]
                    promosion_amount[key] = temp + order[4]
                    temp = 0
                else:
                    promosion_amount[key] = order[4]

    unique_customers = len(set(customers_list))
    avg_discount_rate = total_discount_rate / total_number_of_orders
    avg_order_total = total_amount / total_number_of_orders

    return_statement = {'customers': unique_customers,
                        'total_discount_amount': total_discount_of_the_day,
                        'items': total_products_sold,
                        'order_total_avg': avg_order_total,
                        'discount_rate_avg': avg_discount_rate,
                        'commissions="promotions': {'promotions':{ '1': promosion_amount[1],
                                                                   '2': promosion_amount[2],
                                                                   '3': promosion_amount[3],
                                                                   '4': promosion_amount[4],
                                                                   '5': promosion_amount[5]
                                                                }
                                                    },
                        'total': total_commissions_of_the_day,
                        'order_average':avg_commissions_of_the_day
                        }
    

    return jsonify(
        {
            'customers': unique_customers,
            'total_discount_amount': total_discount_of_the_day,
            'items': total_products_sold,
            'order_total_avg': avg_order_total,
            'discount_rate_avg': avg_discount_rate,
            'commissions="promotions': 
            {
                'promotions':{ '1': promosion_amount[1],
                '2': promosion_amount[2],
                '3': promosion_amount[3],
                '4': promosion_amount[4],
                '5': promosion_amount[5]
            }
                                                    },
            'total': total_commissions_of_the_day,
            'order_average':avg_commissions_of_the_day
        }
    )


def vendor_rate_by_date(date):
    """
    Returns a dictionary with the rates per vendor for a specific date.
    """
    rate_per_vendor = {}

    vendor_commissions = VendorCommissions.query.filter_by(date=date).all()

    for vendor in vendor_commissions:
        rate_per_vendor[vendor.vendor_id] = vendor.rate

    return rate_per_vendor


def order_per_vendor(date):
    """
    Returns a dictionary with vendor id per order id for a specific date.
    """
    order_id_per_vendor = {}

    orders_per_day = Order.query.filter_by(created_at=date).all()

    for order in orders_per_day:
        order_id_per_vendor[order.id] = order.vendor_id
    
    return order_id_per_vendor

def total_and_avg_of_commission(date):
    """
    Returns the average and total amount of commissions for a specific date.
    """
    vendor_per_order = order_per_vendor(date)
    vendors_rates = vendor_rate_by_date(date)
    average_of_commissions = ()
    
    for k, v in vendor_per_order.items():
        total_amount_commission = 0
        orders = OrderLine.query.filter_by(order_id=k).all()
        
        for item in orders:
            total_amount_commission += item.total_amount * vendors_rates[9]
        
    average_of_commissions = total_amount_commission /  len(vendor_per_order.keys())
    avg_and_total = (total_amount_commission, average_of_commissions)
    return avg_and_total


def total_amount_per_promotion(date):
    """
    Returns a product list as part of each promotion
    """
    promotion_dict = defaultdict(list)
    promotions = ProductPromotion.query.filter_by(date=date).all()

    for promotion in promotions:
        promotion_dict[promotion.promotion_id].append(promotion.product_id)
    
    return promotion_dict
