import logging
from functools import wraps

from jwt import JWTValidationError, JWTToken


def need_auth(basic_auth, *permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(handler, *args, **kwargs):
            auth_header = basic_auth
            if auth_header == "null":
                # no header
                logging.info("Authorization header is blank")
                return
            try:
                # trying to get token from `Bearer <token>` string
                token = auth_header.split(" ")[1]
            except IndexError:
                logging.info("Cannot parse header. header: {}"
                             .format(auth_header))
                return

            # Start JWT validation
            try:
                # parsing
                jwt_token = JWTToken(token)
            except JWTValidationError:
                logging.info("Cannot parse header. header: {}"
                             .format(auth_header))
                return

            try:
                # validation
                jwt_token.is_valid()
            except JWTValidationError:
                logging.info("JWT Token invalid. header: {}"
                             .format(auth_header))
                return

            try:
                # permissions
                jwt_token.has_permissions(*permissions)
                return func(handler, *args, **kwargs)
            except JWTValidationError:
                logging.info("No permissions. header: {}"
                             .format(auth_header))

        return wrapper

    return decorator
