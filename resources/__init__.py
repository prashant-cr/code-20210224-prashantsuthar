from flask_cors import CORS
from flask_restful import Api
from resources.healthcheck import HealthCheck


def create_api(app):
    """
    This function creates the apis with CORS Pre-flight request.
    :param app:
    :return:
    """
    # added cors as it was only giving pre-flight request
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    api = Api(app, prefix='/api/')
    api.add_resource(HealthCheck, "healthcheck")
