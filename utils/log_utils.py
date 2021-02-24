import os
import uuid
import flask
import logging
import logging.config


from functools import wraps
from logging import Formatter
from flask import current_app as app
from logging.handlers import TimedRotatingFileHandler


def function_logger(func):
    """
    This is function logger used as the wrapper function to all the business logic functions.
    :param func:
    :return:
    """
    @wraps(func)
    def function_log(*args, **kwargs):
        app.logger.debug(
            "Inside Function {} with parameters: {},{}".format(
                func.__name__,
                args,
                kwargs
            )
        )
        return_param = func(*args, **kwargs)
        app.logger.debug(
            "Function: {} returns {}".format(
                func.__name__,
                return_param
            )
        )
        return return_param

    return function_log


def config_logger(app):
    """
    This function used to configure the logger using logger dict.
    :param app:
    :return:
    """
    file_log_config = app.config['FILE_LOG_CONFIG']
    log_file_path = '%s/%s' % (file_log_config['local_logdir_path'], file_log_config['filename'])
    file_log_handler = TimedRotatingFileHandler(
        log_file_path,
        **file_log_config["kwargs"]
    )

    file_log_handler.setFormatter(Formatter(
        file_log_config['formatter_string']
    ))

    logging_filter = logging.Filter()
    logging_filter.filter = RequestIdFilter().filter

    app.logger.addFilter(logging_filter)
    app.logger.addHandler(file_log_handler)
    app.logger.setLevel(file_log_config['loglevel'])
    app.logger.info("logger configured.!!!")


def os_environ(variable, default=None):
    value = os.getenv(variable, default)
    if value is None:
        raise Exception("Environment Variable %s needs to be set." % variable)

    return value


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if flask.has_request_context():
            record.request_id = request_id()
        else:
            record.request_id = request_id()
        return True


original_log_id = ''
log_id = ''


def _generate_request_id(original_id=''):
    new_id = uuid.uuid4()
    if original_id:
        new_id = "{},{}".format(original_id, new_id)

    return new_id


def request_id():
    """
    This function used to get the unique time stamp for the each request.
    :return:
    """
    global log_id
    global original_log_id

    if flask.has_request_context():
        if log_id is not None and log_id != '' and getattr(flask.g, 'request_id', None) == log_id:
           return log_id
        headers = flask.request.headers
        original_log_id = headers.get("X-Request-Id")
        new_uuid = _generate_request_id(original_log_id)
        flask.g.request_id = new_uuid
        log_id = new_uuid

    if not log_id:
        new_uuid = _generate_request_id()
        log_id = new_uuid

    return log_id
