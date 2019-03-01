from datetime import datetime

from marketplace import db
from marketplace.persistence import constants


# Base model that for other models to inherit from
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.String(constants.CONST_STR_128))
    created_by = db.Column(db.String(constants.CONST_STR_128))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Merchant(Base):
    # field __tablename__ will shown as real tablename on DBMS.
    __tablename__ = 'merchant'

    # field name will assigned as unique and non-nullable.
    name = db.Column(db.String(constants.CONST_STR_128), unique=True, nullable=False)

    description = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=False)
    city = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=False)


class Customer(Base):
    __tablename__ = 'customer'
    name = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=False)
    phone = db.Column(db.String(constants.CONST_STR_16), unique=False, nullable=False)


class Product(Base):
    __tablename__ = 'product'
    name = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=False)


class Transaction(Base):
    __tablename__ = 'order'
    name = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=False)
