from marketplace import ma
from marketplace.persistence.model import ProductCategory, ProductItem, ProductPricing

class ProductCategorySchema(ma.Schema):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'parent_id', 'description', 'created_at', 'updated_at')

class ProductItemSchema(ma.Schema):
    class Meta:
        model = ProductItem
        fields = ('id', 'seller_id', 'category_id', 'name', 'description', 'price', 
                 'currency', 'stock_quantity', 'status', 'images', 'tags', 'sku', 
                 'attributes', 'created_at', 'updated_at')

class ProductPricingSchema(ma.Schema):
    class Meta:
        model = ProductPricing
        fields = ('id', 'product_id', 'base_price', 'discount_price', 'currency',
                 'valid_from', 'valid_to', 'created_at', 'updated_at')

# Initialize schemas
category_schema = ProductCategorySchema()
categories_schema = ProductCategorySchema(many=True)
product_schema = ProductItemSchema()
products_schema = ProductItemSchema(many=True)
pricing_schema = ProductPricingSchema()
pricings_schema = ProductPricingSchema(many=True) 