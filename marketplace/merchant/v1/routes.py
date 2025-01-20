from flask import request
from flask_restx import Resource, Namespace, fields

from marketplace import db
from marketplace.auth.utils import token_required
from marketplace.merchant.v1.serializers import merchant_schema, merchants_schema
from marketplace.persistence.model import Merchant

# Create namespace
merchant_ns = Namespace('merchants', description='Merchant operations')

# API models
merchant_model = merchant_ns.model('Merchant', {
    'name': fields.String(required=True, description='Merchant name'),
    'description': fields.String(required=False, description='Merchant description'),
    'city': fields.String(required=True, description='City location')
})

merchant_response = merchant_ns.model('MerchantResponse', {
    'id': fields.Integer(description='Merchant ID'),
    'name': fields.String(description='Merchant name'),
    'description': fields.String(description='Merchant description'),
    'city': fields.String(description='City location'),
    'owner_id': fields.Integer(description='Owner user ID'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})


@merchant_ns.route('/')
class MerchantList(Resource):
    @merchant_ns.doc('list_merchants')
    @merchant_ns.response(200, 'Success', [merchant_response])
    def get(self):
        """List all merchants"""
        merchants = Merchant.query.all()
        return merchants_schema.dump(merchants)

    @merchant_ns.doc('create_merchant')
    @merchant_ns.expect(merchant_model)
    @merchant_ns.response(201, 'Merchant created', merchant_response)
    @merchant_ns.response(400, 'Validation error')
    @merchant_ns.doc(security='apikey')
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


@merchant_ns.route('/<int:id>')
@merchant_ns.param('id', 'The merchant identifier')
class MerchantResource(Resource):
    @merchant_ns.doc('get_merchant')
    @merchant_ns.response(200, 'Success', merchant_response)
    @merchant_ns.response(404, 'Merchant not found')
    def get(self, id):
        """Get a merchant by ID"""
        merchant = Merchant.query.get(id)
        if not merchant:
            return {'message': 'Merchant not found'}, 404
        return merchant_schema.dump(merchant)

    @merchant_ns.doc('update_merchant')
    @merchant_ns.expect(merchant_model)
    @merchant_ns.response(200, 'Success', merchant_response)
    @merchant_ns.response(404, 'Merchant not found')
    @merchant_ns.doc(security='apikey')
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

    @merchant_ns.doc('delete_merchant')
    @merchant_ns.response(204, 'Merchant deleted')
    @merchant_ns.response(404, 'Merchant not found')
    @merchant_ns.doc(security='apikey')
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
