from flask import jsonify, request
from flask_restx import Resource, Api, Namespace, fields

from marketplace.user.v1 import user_bp
from marketplace.persistence.model import User
from marketplace.user.v1.serializers import user_schema

# Create API namespace
api = Api(user_bp, 
    version='1.0', 
    title='Flask Marketplace API',
    description='A simple marketplace API',
    doc='/swagger'
)

ns = Namespace('auth', description='Authentication operations')
api.add_namespace(ns, path='/auth')

# API models
login_model = ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

login_response = ns.model('LoginResponse', {
    'token': fields.String(description='JWT token'),
    'username': fields.String(description='Username')
})

@ns.route('/login')
class UserLogin(Resource):
    @ns.doc('login')
    @ns.expect(login_model)
    @ns.response(200, 'Success', login_response)
    @ns.response(401, 'Invalid credentials')
    def post(self):
        """User login endpoint"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            return {
                'token': 'dummy-token',  # Implement proper JWT here
                'username': user.username
            }
        return {'message': 'Invalid credentials'}, 401
