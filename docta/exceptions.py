from functools import wraps


def suppress(*exceptions):
    """
    Function decorator suppressing specified exceptions.
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                return
        return inner
    return wrapper
