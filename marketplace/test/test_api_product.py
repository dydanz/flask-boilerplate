import json
from unittest.mock import patch
from uuid import uuid4

from marketplace.persistence.model import User, ProductCategory, ProductItem, ProductPricing, ProductStatus
from marketplace.test import BaseTestCase, Constants

def init_product_data():
    # Create test user
    user = User()
    user.username = Constants.USERNAME
    user.password = Constants.PASSWORD
    user.phone = Constants.PHONE_NUMBER
    user.save()

    # Create test category
    category = ProductCategory()
    category.name = "Test Category"
    category.description = "Test Category Description"
    category.save()

    # Create test product
    product = ProductItem()
    product.seller_id = uuid4()
    product.category_id = category.id
    product.name = "Test Product"
    product.description = "Test Product Description"
    product.price = 100.00
    product.currency = "USD"
    product.stock_quantity = 10
    product.status = ProductStatus.ACTIVE
    product.sku = "TEST-SKU-001"
    product.save()

    # Create test pricing
    pricing = ProductPricing()
    pricing.product_id = product.id
    pricing.base_price = 100.00
    pricing.currency = "USD"
    pricing.valid_from = "2024-01-01T00:00:00"
    pricing.save()

    return category, product, pricing

class ProductApiTestCase(BaseTestCase):
    @patch('marketplace.auth.utils.token_required')
    def test_get_categories_ok(self, mock_auth):
        category, _, _ = init_product_data()
        
        response = self.client.get('/api/v1/product/categories')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(data[0]['name'], "Test Category")

    @patch('marketplace.auth.utils.token_required')
    def test_create_category_ok(self, mock_auth):
        mock_auth.return_value = True
        
        payload = {
            "name": "New Category",
            "description": "New Category Description"
        }
        
        response = self.client.post(
            '/api/v1/product/categories',
            data=json.dumps(payload),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer test-token'
            }
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "New Category")

    @patch('marketplace.auth.utils.token_required')
    def test_get_products_ok(self, mock_auth):
        _, product, _ = init_product_data()
        
        response = self.client.get('/api/v1/product/items')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(data[0]['name'], "Test Product")

    @patch('marketplace.auth.utils.token_required')
    def test_create_product_ok(self, mock_auth):
        category, _, _ = init_product_data()
        mock_auth.return_value = True
        
        payload = {
            "seller_id": str(uuid4()),
            "category_id": str(category.id),
            "name": "New Product",
            "description": "New Product Description",
            "price": 200.00,
            "currency": "USD",
            "stock_quantity": 20,
            "sku": "TEST-SKU-002"
        }
        
        response = self.client.post(
            '/api/v1/product/items',
            data=json.dumps(payload),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer test-token'
            }
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "New Product")

    @patch('marketplace.auth.utils.token_required')
    def test_get_pricing_ok(self, mock_auth):
        _, _, pricing = init_product_data()
        
        response = self.client.get('/api/v1/product/pricing')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(float(data[0]['base_price']), 100.00)

    @patch('marketplace.auth.utils.token_required')
    def test_create_pricing_ok(self, mock_auth):
        _, product, _ = init_product_data()
        mock_auth.return_value = True
        
        payload = {
            "product_id": str(product.id),
            "base_price": 150.00,
            "currency": "USD",
            "valid_from": "2024-01-01T00:00:00"
        }
        
        response = self.client.post(
            '/api/v1/product/pricing',
            data=json.dumps(payload),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer test-token'
            }
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(float(data['base_price']), 150.00) 