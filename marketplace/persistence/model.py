from datetime import datetime
import uuid
import bcrypt
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from sqlalchemy.types import Enum as SQLEnum
import enum
from marketplace import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

class Merchant(db.Model):
    __tablename__ = 'merchants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(256))
    city = db.Column(db.String(128))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    owner = db.relationship('User', backref=db.backref('merchants', lazy=True))

    def save(self):
        db.session.add(self)
        db.session.commit()

class ProductStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"
    DELETED = "deleted"

class ProductCategory(db.Model):
    __tablename__ = 'product_categories'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product_categories.id'), nullable=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Self-referential relationship for hierarchical categories
    children = db.relationship('ProductCategory', 
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')

class ProductItem(db.Model):
    __tablename__ = 'product_items'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = db.Column(UUID(as_uuid=True), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product_categories.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    status = db.Column(SQLEnum(ProductStatus), default=ProductStatus.ACTIVE)
    images = db.Column(ARRAY(db.String), default=[])
    tags = db.Column(ARRAY(db.String), default=[])
    sku = db.Column(db.String(50), unique=True)
    attributes = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = db.relationship('ProductCategory', backref='products')
    pricing_history = db.relationship('ProductPricing', backref='product', lazy='dynamic')

class ProductPricing(db.Model):
    __tablename__ = 'product_pricing'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product_items.id'), nullable=False)
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    discount_price = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(3), nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_to = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserSession:
    """Mock class for testing"""
    pass
