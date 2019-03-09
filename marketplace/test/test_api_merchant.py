import json
from unittest.mock import patch

from marketplace.persistence.model import Merchant, User, UserSession
from marketplace.test import BaseTestCase, Constants


def init_data():

    user = User()
    user.username = Constants.USERNAME
    user.password = Constants.PASSWORD
    user.phone = Constants.PHONE_NUMBER
    user.save()

    merchant = Merchant()
    merchant.name = Constants.MERCHANT_NAME
    merchant.description = Constants.MERCHANT_DESC
    merchant.city = Constants.MERCHANT_CITY
    merchant.save()


class MerchantApiTestCase(BaseTestCase):

    # This decorator will mock a function authorize_user_token()
    @patch('marketplace.v1.authorize_user_token')
    def test_get_merchant_list_ok(self, mock_session):
        # Init required data for testing purpose
        init_data()

        # mock'ed authorize_user_token() will return this value
        mock_session.return_value = UserSession()

        uri = '/api/v1/merchant/data?id=1'

        response = self.client.get(uri, headers={
            'Content-Type': 'application/json',
            'auth-token-key': "ABCDEFGH12345",
            'username-key': '{}'.format(Constants.USERNAME)})

        # Assert HTTP Response
        self.assertEquals(response.status_code, 200)
        json_result = json.loads(response.data)
        self.assertEquals(json_result.get('merchant_name'), Constants.MERCHANT_NAME)

    @patch('marketplace.v1.authorize_user_token')
    def test_get_merchant_list_nok(self, mock_session):
        # Init required data for testing purpose
        init_data()

        # mock'ed authorize_user_token() will return this value
        mock_session.return_value = UserSession()

        uri = '/api/v1/merchant/data?id=2'

        response = self.client.get(uri, headers={
            'Content-Type': 'application/json',
            'auth-token-key': "ABCDEFGH12345",
            'username-key': '{}'.format(Constants.USERNAME)})

        # Assert HTTP Response
        self.assertEquals(response.status_code, 404)
