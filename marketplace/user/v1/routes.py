from flask import jsonify, request
from flask_restx import Resource, Api, Namespace, fields

from marketplace.user.v1 import user_bp
from marketplace.persistence.model import User
from marketplace.user.v1.serializers import user_schema, users_schema
from marketplace.auth.utils import token_required, admin_required, generate_token

# Create API namespace
api = Api(user_bp, 
    version='1.0', 
    title='Flask Marketplace API',
    description='A simple marketplace API',
    doc='/swagger'
)

# Auth namespace for login/register
auth_ns = Namespace('auth', description='Authentication operations')
api.add_namespace(auth_ns, path='/auth')

# Users namespace for CRUD operations
users_ns = Namespace('users', description='User operations')
api.add_namespace(users_ns, path='/users')

# API models
login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

user_create_model = users_ns.model('UserCreate', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'fullname': fields.String(required=True, description='Full Name'),
    'phone': fields.String(required=True, description='Phone Number')
})

user_update_model = users_ns.model('UserUpdate', {
    'fullname': fields.String(description='Full Name'),
    'phone': fields.String(description='Phone Number'),
    'password': fields.String(description='New Password')
})

user_response = users_ns.model('User', {
    'id': fields.Integer(description='User ID'),
    'username': fields.String(description='Username'),
    'fullname': fields.String(description='Full Name'),
    'phone': fields.String(description='Phone Number'),
    'created_at': fields.DateTime(description='Creation Date'),
    'updated_at': fields.DateTime(description='Last Update Date')
})

login_response = auth_ns.model('LoginResponse', {
    'token': fields.String(description='JWT token'),
    'username': fields.String(description='Username')
})

# Auth Routes
@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.doc('login')
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Success', login_response)
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """User login endpoint"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            token = generate_token(user.id)
            return {
                'token': token,
                'username': user.username
            }
        return {'message': 'Invalid credentials'}, 401

# User CRUD Routes
@users_ns.route('/')
class UserList(Resource):
    @users_ns.doc('list_users')
    @users_ns.response(200, 'Success', [user_response])
    @users_ns.doc(security='apikey')
    @admin_required
    def get(self, current_user):
        """List all users (Admin only)"""
        users = User.query.all()
        return users_schema.dump(users)

    @users_ns.doc('create_user')
    @users_ns.expect(user_create_model)
    @users_ns.response(201, 'User created', user_response)
    @users_ns.response(400, 'Validation error')
    def post(self):
        """Create a new user (Public endpoint for registration)"""
        data = request.get_json()
        
        if User.query.filter_by(username=data.get('username')).first():
            return {'message': 'Username already exists'}, 400

        user = User()
        user.username = data.get('username')
        user.password = data.get('password')
        user.fullname = data.get('fullname')
        user.phone = data.get('phone')

        try:
            user.save()
            return user_schema.dump(user), 201
        except Exception as e:
            return {'message': str(e)}, 400

@users_ns.route('/<string:username>')
@users_ns.param('username', 'The user identifier')
class UserResource(Resource):
    @users_ns.doc('get_user')
    @users_ns.response(200, 'Success', user_response)
    @users_ns.response(404, 'User not found')
    @users_ns.doc(security='apikey')
    @token_required
    def get(self, current_user, username):
        """Get a user by username (Auth required)"""
        # Only admin or the user themselves can view details
        if not current_user.is_admin and current_user.username != username:
            return {'message': 'Access denied'}, 403
            
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user)

    @users_ns.doc('update_user')
    @users_ns.expect(user_update_model)
    @users_ns.response(200, 'Success', user_response)
    @users_ns.response(404, 'User not found')
    @users_ns.doc(security='apikey')
    @token_required
    def put(self, current_user, username):
        """Update a user (Auth required)"""
        if not current_user.is_admin and current_user.username != username:
            return {'message': 'Access denied'}, 403
            
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404

        data = request.get_json()
        if 'fullname' in data:
            user.fullname = data['fullname']
        if 'phone' in data:
            user.phone = data['phone']
        if 'password' in data:
            user.password = data['password']

        try:
            user.save()
            return user_schema.dump(user)
        except Exception as e:
            return {'message': str(e)}, 400

    @users_ns.doc('delete_user')
    @users_ns.response(204, 'User deleted')
    @users_ns.response(404, 'User not found')
    @users_ns.doc(security='apikey')
    @admin_required
    def delete(self, current_user, username):
        """Delete a user (Admin only)"""
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404

        try:
            db.session.delete(user)
            db.session.commit()
            return '', 204
        except Exception as e:
            return {'message': str(e)}, 400

# Add security definitions to Swagger UI
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api.authorizations = authorizations
