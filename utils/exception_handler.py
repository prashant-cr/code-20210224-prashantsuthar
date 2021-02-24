from functools import wraps
from flask_restful import abort
from werkzeug.exceptions import UnprocessableEntity
from flask import current_app as app


class NotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def handle_exceptions(fn):
    """
    This is a wrapper function for exception handling. This function used in all the resource layer api functions.
    :param fn:
    :return:
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValueError as message:
            app.logger.error(message)
            return abort(400, message=str(message))

        except KeyError as key_err:
            app.logger.error(key_err)
            return abort(400, message=str(key_err))

        except NotFoundError as nf_err:
            app.logger.error(nf_err.message)
            return abort(404, message=str(nf_err))

        except IOError as io_err:
            app.logger.error(io_err)
            return abort(500, message="IO-ERROR")

        except UnprocessableEntity as sa_err:
            app.logger.error(sa_err)
            try:
                message = sa_err.data.get("messages", None)
            except Exception as sa_err:
                message = sa_err
            abort(422, message=str(message))

        except Exception as exc:
            app.logger.error(exc)
            abort(500, message="INTERNAL-ERROR")

    return wrapper
