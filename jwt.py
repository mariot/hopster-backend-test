import hashlib
import hmac
import json
import time
import logging
from base64 import b64encode, b64decode, urlsafe_b64encode

JWT_SECRET = 'secret'
JWT_DEFAULT_PERMISSIONS = ["insert", "read"]
JWT_SECONDS_EXPIRY_TIME = 60 * 15


class JWTValidationError(Exception):
    def __init__(self, message, *args, **kwargs):
        super(JWTValidationError, self).__init__(*args, **kwargs)
        self.message = message


class JWTToken:
    def __init__(self, token):
        self.token = token
        self.decoded_header = None
        self.decoded_payload = None
        self.parsed_header = None
        self.parsed_payload = None
        self.signature = None
        self._parse()

    def is_valid(self):
        # check expire time
        if self.parsed_payload.get("exp", 0) < int(time.time()):
            raise JWTValidationError(message="Token expired")

        # check signature
        signature = JWT.construct_signature(self.decoded_header,
                                            self.decoded_payload)
        if signature != self.signature:
            logging.info(signature)
            logging.info(self.signature)
            raise JWTValidationError("Invalid token!")

    def has_permissions(self, *permissions):

        for permission in permissions:
            if permission not in self.parsed_payload["permissions"]:
                raise JWTValidationError("Permission denied for {}"
                                         .format(permission))

    def _parse(self):
        try:
            header, payload, signature = self.token.split(".")
        except ValueError:
            raise JWTValidationError(message="Invalid auth token")
        try:
            self.decoded_header = b64decode(header)
            self.decoded_payload = b64decode(payload)
        except TypeError:
            raise JWTValidationError(message="Cannot decode token")
        try:
            self.parsed_header = json.loads(self.decoded_header)
            self.parsed_payload = json.loads(self.decoded_payload)
        except ValueError:
            raise JWTValidationError(message="Cannot load data from token")

        self.signature = signature


class JWT:
    def __new__(cls, *args, **kwargs):
        raise NotImplemented("Use classmethods instead of JWT instance")

    @classmethod
    def create_token(cls, email, *permissions):
        header = cls.construct_header()
        payload = cls.construct_payload(email, *permissions)
        signature = cls.construct_signature(header, payload)
        return b64encode(header) + "." + b64encode(payload) + "." + signature

    @classmethod
    def construct_header(cls, alg="HS256"):
        return json.dumps({
            "typ": "JWT",
            "alg": alg
        })

    @classmethod
    def construct_payload(cls, email, *permissions):
        return json.dumps(
            {
                "exp": int(time.time()) + JWT_SECONDS_EXPIRY_TIME,
                "iss": "hopster",
                "jti": email,
                "permissions": permissions
            }
        )

    @classmethod
    def construct_signature(cls, header, payload):
        encoded_string = urlsafe_b64encode(header) + "."
        encoded_string += urlsafe_b64encode(payload)
        signature = b64encode(hmac.new(JWT_SECRET, encoded_string,
                                       hashlib.sha256).digest())
        return signature
