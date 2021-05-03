from app import db
from datetime import datetime

"""
The following classes are the programatical
representation of the database
"""


class Order(db.Model):
    __tablename__='order'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True)
    vendor_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    order_lines = db.relationship('OrderLine', backref='orders', lazy='dynamic')


class OrderLine(db.Model):
    __tablename__ = 'order_line'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_description = db.Column(db.String(120), nullable=True)
    product_price = db.Column(db.Integer, nullable=False)
    product_vat_rate = db.Column(db.Float, nullable=False)
    discount_rate = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    full_price_amount = db.Column(db.Integer, nullable=False)
    discounted_amount = db.Column(db.Float, nullable=False)
    vat_amount = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)


class Products(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=True)
    order_lines = db.relationship('OrderLine', backref='product', lazy='dynamic')
    products_promotion = db.relationship('ProductPromotion', backref='products', lazy='dynamic')


class Promotion(db.Model):
    __tablename='promotion'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=True)
    product_promotions = db.relationship('ProductPromotion', backref='promotions', lazy='dynamic')


class ProductPromotion(db.Model):
    __tablename__='product_promotion'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True)
    product_id = product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=False)


class VendorCommissions(db.Model):
    __tablename__='vendor_commisssions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True)
    vendor_id = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Float, nullable=False)
