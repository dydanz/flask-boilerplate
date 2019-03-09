from unittest.mock import patch

from flask import json

from marketplace.persistence.model import Merchant, User, UserSession
from marketplace.test import BaseTestCase, Constants


def init_data():
    user = User()
    user.username = Constants.USERNAME
    user.password = Constants.PASSWORD
    user.phone = Constants.PHONE_NUMBER
    user.save()

    merchant = Merchant()
    merchant.name = 'Merchant Test'
    merchant.description = 'Merchant Test Description'
    merchant.city = 'Jakarta'
    merchant.save()


class UserApiTestCase(BaseTestCase):

    @patch('marketplace.v1.authorize_user_token')
    def test_get_user_data_ok(self, mock_session):
        pass

    @patch('marketplace.v1.authorize_user_token')
    def test_post_user_login_ok(self, mock_session):
        init_data()
        mock_session.return_value = UserSession()

        uri = '/api/v1/user/auth/login'

        post_data = {
            "username": Constants.USERNAME,
            "password": Constants.PASSWORD
        }

        response = self.client.post(uri, data=json.dumps(post_data),
                                    headers={
                                        'Content-Type': 'application/json',
                                        'auth-token-key': '',
                                        'username-key': '{}'.format(Constants.USERNAME)})

        # Assert HTTP Response
        self.assertEquals(response.status_code, 200)
        json_result = json.loads(response.data)
        self.assertEquals(json_result.get('username'), 'testuser')
