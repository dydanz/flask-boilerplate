from flask import Blueprint, jsonify
from flask_restx import Api, Resource, Namespace, fields
from marketplace import db

health_bp = Blueprint('health', __name__)
api = Api(health_bp,
    version='1.0',
    title='Health Check API',
    description='API Health monitoring endpoints',
    doc='/swagger'
)

ns = Namespace('health', description='Health check operations')
api.add_namespace(ns)

health_response = ns.model('HealthResponse', {
    'status': fields.String(description='Service status'),
    'database': fields.String(description='Database connection status'),
    'message': fields.String(description='Detailed status message')
})

@ns.route('/ping')
class HealthCheck(Resource):
    @ns.doc('health_check')
    @ns.response(200, 'Service is healthy', health_response)
    @ns.response(503, 'Service is unhealthy', health_response)
    def get(self):
        """Check the health status of the service"""
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            return {
                'status': 'healthy',
                'database': 'connected',
                'message': 'Service is running normally'
            }, 200
        except Exception as e:
            return {
                'status': 'unhealthy',
                'database': 'disconnected',
                'message': str(e)
            }, 503 