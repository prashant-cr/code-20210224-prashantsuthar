import os
import sys
import logging
import pwd

BASE_PATH = pwd.getpwuid(os.getuid()).pw_dir

DEFAULT_LOGGER_NAME = 'BMI_Project'
APP_LOG_FILE = 'logs/'

input_file_path = 'input_data.json'

table_config = [
    {
        "Category": "Underweight",
        "HealthRisk": "Malnutrition Risk",
        "bmi": 18.4
    },
    {
        "Category": "Normal Weight",
        "HealthRisk": "Low Risk",
        "bmi": 24.9
    },
    {
        "Category": "Overweight",
        "HealthRisk": "Enhanced risk",
        "bmi": 29.9
    },
    {
        "Category": "Moderately obese",
        "HealthRisk": "Medium risk",
        "bmi": 34.9
    },
    {
        "Category": "Severely obese",
        "HealthRisk": "High risk",
        "bmi": 39.9
    },
    {
        "Category": "Very Severely obese",
        "HealthRisk": "Very high risk",
        "bmi": 40
    }
]

FILE_LOG_CONFIG = {
    'filename': 'logging.log',
    'loglevel': logging.DEBUG,
    'local_logdir_path': APP_LOG_FILE,
    'formatter_string': '%(request_id)s - %(asctime)s - %(filename)s - %(module)s - %(funcName)s - %(lineno)d - '
                        '[%(levelname)s] - %(message)s',
    'kwargs': {
        'utc': True
    }
}
LOGGING_CONFIG = dict(
    version=1,
    filters={
        'request_id': {
            '()': 'utils.logger.RequestIdFilter',
        },
    },
    formatters={
        'compact': {
            'format': '%(asctime)s [%(levelname)s] %(name)-10.10s : %(message)s'
        },
        'verbose': {
            'format': '%(request_id)s - %(asctime)s - %(filename)s - %(module)s - %(funcName)s - '
                      '%(lineno)d - [%(levelname)s] - %(message)s'
        },
        'err_report': {'format': '%(asctime)s\n%(message)s'}
    },
    handlers={
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'compact',
            'filters': ['request_id']
        },
        DEFAULT_LOGGER_NAME: {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filters': ['request_id'],
            'level': 'DEBUG',
            'filename': APP_LOG_FILE
        }
    },
    loggers={
        DEFAULT_LOGGER_NAME: {
            'handlers': [DEFAULT_LOGGER_NAME, 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'crash': {
            'handlers': [DEFAULT_LOGGER_NAME],
            'level': 'ERROR',
            'propagate': False
        },
    }
)

