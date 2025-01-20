from flask_restx import Namespace, Resource, fields
from sqlalchemy.sql import text

from marketplace import db

# Create namespace instead of blueprint
health_ns = Namespace("health", description="Health check operations")

health_response = health_ns.model(
    "HealthResponse",
    {
        "status": fields.String(description="Service status"),
        "database": fields.String(description="Database connection status"),
        "message": fields.String(description="Detailed status message"),
    },
)


@health_ns.route("/ping")
class HealthCheck(Resource):
    @health_ns.doc("health_check")
    @health_ns.response(200, "Service is healthy", health_response)
    @health_ns.response(503, "Service is unhealthy", health_response)
    def get(self):
        """Check the health status of the service"""
        try:
            # Test database connection
            db.session.execute(text("SELECT 1"))
            return {
                "status": "server alive - healthy",
                "database": "connected",
                "message": "Service is running normally",
            }, 200
        except Exception as e:
            return {
                "status": "server alive - unhealthy",
                "database": "disconnected",
                "message": str(e),
            }, 503
