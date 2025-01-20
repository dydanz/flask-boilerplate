# Keep this empty for now

from flask_testing import TestCase
from marketplace import create_app, db

class Constants:
    USERNAME = "testuser"
    PASSWORD = "this15secret"
    PHONE_NUMBER = "+6280123456789"
    MERCHANT_NAME = "Test Merchant"
    MERCHANT_DESC = "Test Description"
    MERCHANT_CITY = "Test City"

class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app('test')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
