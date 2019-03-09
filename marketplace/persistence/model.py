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
    # __tablename__ will shown as real table-name on DBMS, not a table's column.
    __tablename__ = 'merchant'

    # column name will assigned as unique and non-nullable.
    name = db.Column(db.String(constants.CONST_STR_128), unique=True, nullable=False)

    # Owner of Merchant, must be a valid/registered User.
    # Notes it's a Foreign Key to non-primary key, using column 'user.username' as a FK, not using
    # 'user.id' as user's original PK
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=True)

    description = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=False)
    city = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=False)


class Product(Base):
    __tablename__ = 'product'
    name = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=False)
    price = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class Transaction(Base):
    __tablename__ = 'order'
    invoice_no = db.Column(db.String(constants.CONST_STR_128), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    # column username will assigned as unique and non-nullable.
    # index=True means this is an Indexable column with the predefined index to access it.
    username = db.Column(db.String(constants.CONST_STR_64), unique=True, nullable=False, index=True)

    password = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=False)
    fullname = db.Column(db.String(constants.CONST_STR_128), unique=False, nullable=True)
    phone = db.Column(db.String(constants.CONST_STR_16), unique=True, nullable=False)
    email = db.Column(db.String(constants.CONST_STR_16), unique=True, nullable=True)


class UserSession(Base):
    __tablename__ = 'user_session'
    id = db.Column(db.String(constants.CONST_STR_64), primary_key=True,
                   unique=True, nullable=False, index=True)
    username = db.Column(db.String(constants.CONST_STR_64), nullable=False, index=True)
    secret_key = db.Column(db.String(constants.CONST_STR_64), nullable=False, index=True)
