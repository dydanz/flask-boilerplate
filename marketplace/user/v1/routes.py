from flask import jsonify
from flask_restplus import Resource
from flask_restplus.cors import crossdomain
from sqlalchemy import exc

from common.authenticator.session_management import create_user_session, delete_user_session
from common.http import custom_errors as errors
from marketplace import db
from marketplace.persistence.model import User
from marketplace.user.v1.serializers import common_resp_fields, post_user_data_parser, \
    post_user_login_data_parser, post_user_login_data_response, post_user_logout_data_parser
from marketplace.v1 import api, log

ns = api.namespace('user', description='Operations related to User Data')


@ns.route('/data')
class UserDataApi(Resource):
    @crossdomain('*')
    @api.expect(post_user_data_parser, validate=True)
    @api.doc(responses={
        200: ('Success', common_resp_fields),
        400: 'Bad Gateway',
        401: 'Unauthorized',
        404: ('Not Found', None),
        500: 'Internal server error.'
    })
    def post(self):
        args = api.payload

        query_result = User.query.filter(User.username == args.get('username')).first()

        if query_result:
            return errors.bad_request('Username is already used.')

        user = User()
        user.username = args.get('username')
        user.fullname = args.get('fullname')
        user.password = args.get('password')
        user.phone = args.get('phone')

        try:
            user.save()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            log.error('Post User Data failed, ' + str(e))
            return errors.internal_server_error_msg('Post User Data failed')

        return jsonify({
            'status': 'OK',
            'message': 'Post User Data {} is Success'.format(user.username),
        })

    @crossdomain('*')
    @api.expect(post_user_data_parser, validate=True)
    @api.doc(responses={
        200: ('Success', common_resp_fields),
        400: 'Bad Gateway',
        401: 'Unauthorized',
        404: ('Not Found', None),
        500: 'Internal server error.'
    })
    def put(self):
        args = api.payload

        user = User.query.filter(User.username == args.get('username')).first()

        if user is None:
            return errors.bad_request('Username is not found.')

        user.fullname = args.get('fullname', user.fullname)
        user.phone = args.get('phone', user.fullname)
        user.password = args.get('password', user.password)

        try:
            user.save()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            log.error('Update User Data failed, ' + str(e))
            return errors.internal_server_error_msg('Update User Data failed')

        return jsonify({
            'status': 'OK',
            'message': 'Update User Data {} is Success'.format(user.username),
        })


@ns.route('/auth/login')
class UserAuthLoginApi(Resource):
    @crossdomain('*')
    @api.expect(post_user_login_data_parser, validate=True)
    @api.doc(responses={
        200: ('Success', post_user_login_data_response),
        400: 'Bad Gateway',
        401: 'Unauthorized',
        404: ('Not Found', None),
        500: 'Internal server error.'
    })
    def post(self):
        args = api.payload
        user = User.query.filter(User.username == args.get('username')).first()
        if user is None or user.password != args.get('password'):
            errors.abort(401, message='Username or Password is incorrect')

        # Authorization Token will be created and sent to User
        token = create_user_session(user)

        return jsonify({
            'username': user.username,
            'token': token,
        })


@ns.route('/auth/logout')
class UserAuthLogoutApi(Resource):
    @crossdomain('*')
    @api.expect(post_user_logout_data_parser, validate=True)
    @api.doc(responses={
        200: ('Success', common_resp_fields),
        400: 'Bad Gateway',
        401: 'Unauthorized',
        404: ('Not Found', None),
        500: 'Internal server error.'
    })
    def post(self):
        args = api.payload
        user = User.query.filter(User.username == args.get('username')).first()
        if user is None:
            errors.abort(401, message='Username or Password is incorrect')

        delete_user_session(user.username)

        return jsonify({
            'status': 'OK',
            'message': 'User {} is Logged Out'.format(user.username),
        })
