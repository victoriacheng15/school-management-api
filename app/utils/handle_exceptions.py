import logging
from functools import wraps
from app.utils import api_response_error


def handle_exceptions_read(default_status_code=500):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.exception("Unexpected error in read operation.")
                return api_response_error(f"Internal server error: {str(e)}.", default_status_code)
        return wrapper
    return decorator

def handle_exceptions_write(default_status_code=500):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError as e:
                logging.warning(f"Missing required field: {str(e)}")
                return api_response_error(f"Missing required field: {str(e)}.", 400)
            except Exception as e:
                logging.exception("Unexpected error in write operation.")
                return api_response_error(f"Internal server error: {str(e)}.", default_status_code)
        return wrapper
    return decorator
