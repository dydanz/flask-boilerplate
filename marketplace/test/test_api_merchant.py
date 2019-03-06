import json
from unittest.mock import patch

from marketplace.persistence.model import Merchant
from marketplace.test import BaseTestCase

ROOT_PATH = 'http://test.amazonaws.com/merchant-picture-dev/M0000000001/'


def init_data():
    merchant = Merchant()
    merchant.name = 'Merchant Test'
    merchant.description = 'Merchant Test Description'
    merchant.city = 'Jakarta'
    merchant.save()


class MerchantApiTestCase(BaseTestCase):
    def test_get_merchant_list(self):
        init_data()

        uri = '/api/v1/merchant/merchant/data?id=1'

        response = self.client.get(uri, headers={
            'Content-Type': 'application/json',
            'auth-token-key': "ABCDEFGH12345",
            'username-ke': '{}'.format('user1test')})

        self.assertEquals(response.status_code, 200)


