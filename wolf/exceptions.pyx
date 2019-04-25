# cython: language_level=3
from nanohttp import HttpStatus


class ExpiredTokenError(HttpStatus):
    status_code, status_text, info = 461, 'Token is expired', 'The requested token is expired.'


class LockedTokenError(HttpStatus):
    status_code, status_text, info = 462, 'Token is locked', 'The max try limitation is exceeded.'


class DeactivatedTokenError(HttpStatus):
    status_code, status_text, info = 463, 'Token is deactivated', 'Token has been deactivated.'


class DeviceNotFoundError(HttpStatus):
    status_code, status_text, info = 464, 'Device Not Found', 'Requested device is found.'


class ActivatedTokenError(HttpStatus):
    status_code, status_text, info = 465, 'Token is active', 'Token is already active.'


class NotLockedTokenError(HttpStatus):
    status_code, status_text, info = 466, 'Token is not locked', 'The max try limitation is not exceeded.'

