from flask import current_app as app
from flask_restful import Resource
from utils.exception_handler import handle_exceptions
from functionality.bmi_data import get_bmi_info
from webargs.flaskparser import use_kwargs
from marshmallow import Schema, fields as f


class BMI(Resource):
    decorators = [handle_exceptions]

    def __init__(self):
        app.logger.info('In the constructor of {}'.format(self.__class__.__name__))

    @staticmethod
    def get():
        app.logger.info('In get method of BMI')
        response = get_bmi_info()
        return response
