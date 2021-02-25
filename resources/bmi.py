from flask import current_app as app
from flask_restful import Resource
from utils.exception_handler import handle_exceptions
from functionality.bmi_data import get_bmi_info, post_bmi_info
from webargs.flaskparser import use_kwargs
from marshmallow import Schema, fields as f


class DataSchema(Schema):
    gender = f.Str(required=True)
    HeightCm = f.Float(required=True)
    WeightKg = f.Float(required=True)

    class Meta:
        strict = True


class BMIPostSchema(Schema):
    data = f.List(f.Nested(DataSchema, required=True), required=True)

    class Meta:
        strict = True


class BMI(Resource):
    decorators = [handle_exceptions]

    def __init__(self):
        app.logger.info('In the constructor of {}'.format(self.__class__.__name__))

    @staticmethod
    def get():
        app.logger.info('In get method of BMI')
        response = get_bmi_info()
        return response

    @use_kwargs(BMIPostSchema)
    def post(self, **kwargs):
        app.logger.info("IN Post method of Bank info with parameters {}".format(kwargs))
        response = post_bmi_info(**kwargs)
        return response
