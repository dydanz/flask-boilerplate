from flask import jsonify, request
from flask_restplus import Resource
from flask_restplus.cors import crossdomain
from sqlalchemy import exc

from common.http import custom_errors as errors
from marketplace import db
from marketplace.merchant.v1.serializers import common_resp_fields, merchant_list_fields, \
    merchant_pagination_fields, merchant_search_parser, post_merchant_data_parser, \
    put_merchant_data_parser
from marketplace.persistence.model import Merchant
from marketplace.v1 import api, log

ns = api.namespace('merchant', description='Operations related to Merchant Data')


@ns.route('/data')
class MerchantDataApi(Resource):
    @crossdomain('*')
    @api.expect(merchant_search_parser, validate=True)
    @api.doc(responses={
        200: ('Success', merchant_list_fields),
        400: 'Bad Gateway',
        401: 'Unauthorized',
        404: ('Not Found', None),
        500: 'Internal server error.'
    })
    def get(self):
        """
        Get Merchant Data by given ID
        :return: Merchant Details Information
        """
        merchant_id = request.args.get('id', 1, type=int)

        query_result = Merchant.query.filter(Merchant.id == merchant_id).first()

        if query_result is None:
            return errors.not_found('Merchant not found')

        return jsonify({
            'merchant_id': query_result.id,
            'merchant_name': query_result.name,
            'description': query_result.description,
            'city': query_result.city,
        })

    @crossdomain('*')
    @api.expect(post_merchant_data_parser, validate=True)
    @api.doc(responses={
        200: ('Success', common_resp_fields),
        400: 'Bad Gateway',
        401: 'Unauthorized',
        404: ('Not Found', None),
        500: 'Internal server error.'
    })
    def post(self):
        args = api.payload

        query_result = Merchant.query.filter(Merchant.name == args.get('merchant_name')).first()

        if query_result:
            return errors.bad_request('Merchant Name is already used.')

        merchant = Merchant()
        merchant.name = args.get('merchant_name')
        merchant.description = args.get('description')
        merchant.city = args.get('city')

        try:
            merchant.save()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            log.error('Save new Merchant Data failed, ' + str(e))
            return errors.internal_server_error_msg('Save new Merchant Data failed')

        return jsonify({
            'status': 'OK',
            'message': 'Save new Merchant Data {} is Success'.format(merchant.name),
        })

    @crossdomain('*')
    @api.expect(put_merchant_data_parser, validate=True)
    @api.doc(responses={
        200: ('Success', common_resp_fields),
        400: 'Bad Gateway',
        401: 'Unauthorized',
        404: ('Not Found', None),
        500: 'Internal server error.'
    })
    def put(self):
        args = api.payload

        merchant = Merchant.query.filter(Merchant.id == args.get('merchant_id')).first()

        if merchant is None:
            return errors.bad_request('Merchant not found')

        # Get Data from request payload if any, otherwise will assigned to its original value
        merchant.name = args.get('merchant_name', merchant.name)
        merchant.description = args.get('description', merchant.description)
        merchant.city = args.get('city', merchant.city)

        try:
            merchant.save()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            log.error('Update Merchant Data failed, ' + str(e))
            return errors.internal_server_error_msg('Update Merchant data failed')

        return jsonify({
            'status': 'OK',
            'message': 'Update Merchant {} is Success'.format(merchant.name),
        })

    @crossdomain('*')
    @api.expect(merchant_search_parser, validate=True)
    @api.doc(responses={
        200: ('Success', common_resp_fields),
        400: 'Bad Gateway',
        401: 'Unauthorized',
        404: ('Not Found', None),
        500: 'Internal server error.'
    })
    def delete(self):
        """
        DELETE Merchant Data by given ID
        :return: Transaction Status
        """
        merchant_id = request.args.get('id', 1, type=int)

        merchant = Merchant.query.filter(Merchant.id == merchant_id).first()

        if merchant is None:
            return errors.bad_request('Merchant not found')

        try:
            merchant.delete()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            log.error('Delete Merchant failed, ' + str(e))
            return errors.internal_server_error_msg('Delete Merchant failed')

        return jsonify({
            'status': 'OK',
            'message': 'Delete Merchant {} is Success'.format(merchant.name),
        })


@ns.route('/search')
class MerchantSearchApi(Resource):
    @crossdomain('*')
    @api.expect(merchant_search_parser, validate=True)
    @api.doc(responses={
        200: ('Success', merchant_pagination_fields),
        400: 'Bad Gateway',
        401: 'Unauthorized',
        404: ('Not Found', None),
        500: 'Internal server error.'
    })
    def get(self):
        response = []
        page = request.args.get('page', 1, type=int)
        results_per_page = request.args.get('results_per_page', 10, type=int)
        keywords = request.args.get('keywords')

        # Will Query Merchants matches with given keyword(s) and paginate the query result.
        query_result = Merchant.query.filter(
                Merchant.merchant_name.ilike('%' + keywords + '%')).paginate(page, results_per_page)

        for merchant in query_result.items:
            response.append({
                'merchant_id': merchant.merchant_id,
                'merchant_name': merchant.merchant_name})

        return jsonify({
            'merchants': response, 'page': page,
            'total_pages': query_result.total_pages if query_result else 0,
            'results_per_page': results_per_page
        })
