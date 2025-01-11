from flask import Blueprint, request
from flask_restx import Api, Resource, Namespace, fields
from marketplace import db
from marketplace.persistence.model import Merchant
from marketplace.merchant.v1.serializers import merchant_schema, merchants_schema
from marketplace.auth.utils import token_required, admin_required

merchant_bp = Blueprint('merchant_v1', __name__)

# Create API namespace
api = Api(merchant_bp,
    version='1.0',
    title='Merchant API',
    description='Merchant management operations',
    doc='/swagger'
)

ns = Namespace('merchants', description='Merchant operations')
api.add_namespace(ns)

# API models
merchant_model = ns.model('Merchant', {
    'name': fields.String(required=True, description='Merchant name'),
    'description': fields.String(required=False, description='Merchant description'),
    'city': fields.String(required=True, description='City location')
})

merchant_response = ns.model('MerchantResponse', {
    'id': fields.Integer(description='Merchant ID'),
    'name': fields.String(description='Merchant name'),
    'description': fields.String(description='Merchant description'),
    'city': fields.String(description='City location'),
    'owner_id': fields.Integer(description='Owner user ID'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

@ns.route('/')
class MerchantList(Resource):
    @ns.doc('list_merchants')
    @ns.response(200, 'Success', [merchant_response])
    def get(self):
        """List all merchants"""
        merchants = Merchant.query.all()
        return merchants_schema.dump(merchants)

    @ns.doc('create_merchant')
    @ns.expect(merchant_model)
    @ns.response(201, 'Merchant created', merchant_response)
    @ns.response(400, 'Validation error')
    @ns.doc(security='apikey')
    @token_required
    def post(self, current_user):
        """Create a new merchant (Auth required)"""
        data = request.get_json()
        
        if Merchant.query.filter_by(name=data.get('name')).first():
            return {'message': 'Merchant name already exists'}, 400

        merchant = Merchant(
            name=data.get('name'),
            description=data.get('description'),
            city=data.get('city'),
            owner_id=current_user.id
        )

        try:
            merchant.save()
            return merchant_schema.dump(merchant), 201
        except Exception as e:
            return {'message': str(e)}, 400

@ns.route('/<int:id>')
@ns.param('id', 'The merchant identifier')
class MerchantResource(Resource):
    @ns.doc('get_merchant')
    @ns.response(200, 'Success', merchant_response)
    @ns.response(404, 'Merchant not found')
    def get(self, id):
        """Get a merchant by ID"""
        merchant = Merchant.query.get(id)
        if not merchant:
            return {'message': 'Merchant not found'}, 404
        return merchant_schema.dump(merchant)

    @ns.doc('update_merchant')
    @ns.expect(merchant_model)
    @ns.response(200, 'Success', merchant_response)
    @ns.response(404, 'Merchant not found')
    @ns.doc(security='apikey')
    @token_required
    def put(self, current_user, id):
        """Update a merchant (Auth required)"""
        merchant = Merchant.query.get(id)
        if not merchant:
            return {'message': 'Merchant not found'}, 404

        # Only owner or admin can update
        if not current_user.is_admin and merchant.owner_id != current_user.id:
            return {'message': 'Access denied'}, 403

        data = request.get_json()
        if 'name' in data:
            merchant.name = data['name']
        if 'description' in data:
            merchant.description = data['description']
        if 'city' in data:
            merchant.city = data['city']

        try:
            merchant.save()
            return merchant_schema.dump(merchant)
        except Exception as e:
            return {'message': str(e)}, 400

    @ns.doc('delete_merchant')
    @ns.response(204, 'Merchant deleted')
    @ns.response(404, 'Merchant not found')
    @ns.doc(security='apikey')
    @token_required
    def delete(self, current_user, id):
        """Delete a merchant (Auth required)"""
        merchant = Merchant.query.get(id)
        if not merchant:
            return {'message': 'Merchant not found'}, 404

        # Only owner or admin can delete
        if not current_user.is_admin and merchant.owner_id != current_user.id:
            return {'message': 'Access denied'}, 403

        try:
            db.session.delete(merchant)
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
