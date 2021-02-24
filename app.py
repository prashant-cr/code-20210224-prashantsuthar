import resources

from flask import Flask
from utils.log_utils import config_logger


def create_app():
    """
    This method creates the flask app and configure it.
    :return:
    """
    app = Flask('BMI_Project')
    app.config.from_object('config')
    config_logger(app)
    resources.create_api(app)
    return app


main_app = create_app()

if __name__ == '__main__':
    main_app.run('0.0.0.0', 5050, debug=True)
