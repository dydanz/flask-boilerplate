from flask import request
from flask_restx import Resource, Namespace, fields

from marketplace import db
from marketplace.auth.utils import token_required
from marketplace.persistence.model import (ProductCategory,
                                           ProductItem, ProductPricing)
from marketplace.product.v1.serializers import (
    category_schema, categories_schema,
    product_schema, products_schema,
    pricing_schema, pricings_schema
)

# Create namespaces
category_ns = Namespace('categories', description='Product category operations')
product_ns = Namespace('products', description='Product operations')
pricing_ns = Namespace('pricing', description='Product pricing operations')

# API Models
category_model = category_ns.model('Category', {
    'name': fields.String(required=True, description='Category name'),
    'parent_id': fields.String(required=False, description='Parent category ID'),
    'description': fields.String(required=False, description='Category description')
})

product_model = product_ns.model('Product', {
    'seller_id': fields.String(required=True, description='Seller ID'),
    'category_id': fields.String(required=True, description='Category ID'),
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(required=True, description='Product description'),
    'price': fields.Float(required=True, description='Product price'),
    'currency': fields.String(required=True, description='Currency code'),
    'stock_quantity': fields.Integer(required=True, description='Stock quantity'),
    'images': fields.List(fields.String, description='Image URLs'),
    'tags': fields.List(fields.String, description='Product tags'),
    'sku': fields.String(required=True, description='Stock Keeping Unit'),
    'attributes': fields.Raw(description='Product attributes')
})

pricing_model = pricing_ns.model('Pricing', {
    'product_id': fields.String(required=True, description='Product ID'),
    'base_price': fields.Float(required=True, description='Base price'),
    'discount_price': fields.Float(description='Discount price'),
    'currency': fields.String(required=True, description='Currency code'),
    'valid_from': fields.DateTime(required=True, description='Valid from date'),
    'valid_to': fields.DateTime(description='Valid to date')
})


# Category Routes
@category_ns.route('/')
class CategoryList(Resource):
    @category_ns.doc('list_categories')
    def get(self):
        """List all categories"""
        categories = ProductCategory.query.all()
        return categories_schema.dump(categories)

    @category_ns.doc('create_category')
    @category_ns.expect(category_model)
    @category_ns.response(201, 'Category created')
    @category_ns.doc(security='apikey')
    @token_required
    def post(self, current_user):
        """Create a new category"""
        data = request.get_json()
        category = ProductCategory(**data)
        db.session.add(category)
        db.session.commit()
        return category_schema.dump(category), 201


# Product Routes
@product_ns.route('/')
class ProductList(Resource):
    @product_ns.doc('list_products')
    def get(self):
        """List all products"""
        products = ProductItem.query.all()
        return products_schema.dump(products)

    @product_ns.doc('create_product')
    @product_ns.expect(product_model)
    @product_ns.response(201, 'Product created')
    @product_ns.doc(security='apikey')
    @token_required
    def post(self, current_user):
        """Create a new product"""
        data = request.get_json()
        product = ProductItem(**data)
        db.session.add(product)
        db.session.commit()
        return product_schema.dump(product), 201


# Pricing Routes
@pricing_ns.route('/')
class PricingList(Resource):
    @pricing_ns.doc('list_pricing')
    def get(self):
        """List all pricing records"""
        pricing = ProductPricing.query.all()
        return pricings_schema.dump(pricing)

    @pricing_ns.doc('create_pricing')
    @pricing_ns.expect(pricing_model)
    @pricing_ns.response(201, 'Pricing created')
    @pricing_ns.doc(security='apikey')
    @token_required
    def post(self, current_user):
        """Create a new pricing record"""
        data = request.get_json()
        pricing = ProductPricing(**data)
        db.session.add(pricing)
        db.session.commit()
        return pricing_schema.dump(pricing), 201
