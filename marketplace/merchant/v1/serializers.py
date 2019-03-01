from flask_restplus import fields

from common.http.http_request_parser import CommonParser
from marketplace.v1 import api

common_resp_fields = api.model('common_resp_fields', {
    'status': fields.String(readOnly=True, description='Response Status'),
    'message': fields.String(readOnly=True, description='Response Message Details')
})

'''
Search Merchant Request Payload
'''
merchant_search_parser = CommonParser(oy_token_validate=True).default()
merchant_search_parser.add_argument('keywords', type=str, location='args', required=True,
                                    help='Searching Keywords')
merchant_search_parser.add_argument('page', type=int, location='args', default=1)
merchant_search_parser.add_argument('results_per_page', type=int, location='args', default=10)

'''
Get Merchant Request Payload
'''
merchant_search_parser = CommonParser(oy_token_validate=True).default()
merchant_search_parser.add_argument('id', type=str, location='args', required=True,
                                    help='Merchant ID')

'''
Post Merchant Request Payload
'''
post_merchant_data_parser = api.model('post_merchant_data_parser', {
    'merchant_name': fields.String(example='PetSmart.com', required=True),
    'description': fields.String(example='Pet Store and Grooming', required=False),
    'city': fields.String(example='Jakarta', required=False)
})

'''
PUT Merchant Request Payload
'''
put_merchant_data_parser = api.model('put_merchant_data_parser', {
    'merchant_id': fields.Integer(example=123, required=True),
    'merchant_name': fields.String(example='PetSmart.com', required=False),
    'description': fields.String(example='Pet Store and Grooming', required=True),
    'city': fields.String(example='Jakarta', required=True)
})

'''
Search Merchant Response Payload
'''
merchant_list_fields = api.model('merchant_list_fields', {
    'merchant_id': fields.String(readOnly=True, example='0000000001'),
    'merchant_name': fields.String(readOnly=True, example='PetSmart.com'),
    'description': fields.String(readOnly=True, example='Pet Store and Grooming'),
    'city': fields.String(readOnly=True, example='Jakarta'),
})

merchant_pagination_fields = api.model('merchant-search-response', {
    'page': fields.Integer(readOnly=True, example='1'),
    'total_pages': fields.Integer(readOnly=True, example='6'),
    'results_per_page': fields.Integer(readOnly=True, example='10'),
    'total_rows': fields.Integer(readOnly=True, example='10'),
    'merchants': fields.List(fields.Nested(merchant_list_fields))
})
