from flask_restplus import fields

from marketplace.v1 import api

common_resp_fields = api.model('common_resp_fields', {
    'status': fields.String(readOnly=True, description='Response Status'),
    'message': fields.String(readOnly=True, description='Response Message Details')
})

'''
Post User Request Payload
'''
post_user_data_parser = api.model('post_user_data_parser', {
    'username': fields.String(example='john_doe_1946', required=True),
    'fullname': fields.String(example='John Doe', required=False),
    'password': fields.String(example='this15secret', required=True),
    'phone': fields.String(example='+628123456789', required=True)
})

'''
Put User Request Payload
'''
put_user_data_parser = api.model('put_user_data_parser', {
    'fullname': fields.String(example='John Doe', required=False),
    'phone': fields.String(example='+628123456789', required=False),
    'password': fields.String(example='this15secret', required=False)
})

'''
Post User Login Request Payload
'''
post_user_login_data_parser = api.model('post_user_login_data_parser', {
    'username': fields.String(example='john_doe_1946', required=True),
    'password': fields.String(example='this15secret', required=True)
})

'''
Post User Login Response Payload
'''
post_user_login_data_response = api.model('post_user_login_data_response', {
    'username': fields.String(readOnly=True, example='0000000001'),
    'token': fields.String(
            readOnly=True,
            example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9'
                    '.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg')
})

'''
Post User Logout Request Payload
'''
post_user_logout_data_parser = api.model('post_user_logout_data_parser', {
    'username': fields.String(example='john_doe_1946', required=True),
    'token': fields.String(
            readOnly=True,
            example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9'
                    '.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg')
})
