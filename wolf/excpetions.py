from nanohttp import HttpStatus


class ExpiredTokenError(HttpStatus):
    status_code, status_text, info = 461, 'Token is expired', 'The requested token is expired.'


class LockedTokenError(HttpStatus):
    status_code, status_text, info = 462, 'Token is locked', 'The max try limitation is exceeded.'


class DeviceNotFoundError(HttpStatus):
    status_code, status_text, info = 464, 'Device Not Found', 'Requested device is found.'
