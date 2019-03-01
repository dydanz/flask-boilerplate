from flask_restplus.reqparse import RequestParser


class CommonParser:
    def __init__(self, oy_token_validate=False):
        self.parser = RequestParser()
        if oy_token_validate:
            self.parser.add_argument('auth-token-key', required=True, location='headers',
                                     help='User Authorization Token')
            self.parser.add_argument('username-key', required=True, location='headers',
                                     help='Username of Token Owner')

    def default(self):
        return self.parser
