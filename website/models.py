from sqlalchemy.orm import backref
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Roles(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), unique=True)
    users = db.relationship('User', backref='role', lazy=True)


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(128))
    description = db.Column(db.String(250))
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    pgp_key = db.Column(db.Text)
    products = db.relationship('Products', backref='user', lazy=True)
    carts = db.relationship('Cart')
    support = db.relationship('Support')
    user_ratings = db.relationship('UserRating')


    def get_id(self):
           return (self.user_id)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(250))
    price = db.Column(db.Integer)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    quantity = db.Column(db.Integer)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    carts = db.relationship('Cart')
    user_ratings = db.relationship('UserRating')

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    name = db.Column(db.String(20))
    street = db.Column(db.String(20))
    house_number = db.Column(db.Integer)
    zip_code = db.Column(db.String(20))
    city = db.Column(db.String(20))
    completed = db.Column(db.Boolean, default=False)

class Cart(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    product = db.Column(db.Integer, db.ForeignKey('products.id'))

class UserRating(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    text = db.Column(db.String(250))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.username'))
    product = db.Column(db.Integer, db.ForeignKey('products.id'))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    email = db.Column(db.String(20))
    subject = db.Column(db.String(20))
    text = db.Column(db.String(500))

class Support(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    subject = db.Column(db.String(20))
    text = db.Column(db.String(500))
    image_file = db.Column(db.String(20), nullable=False)