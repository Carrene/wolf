from nanohttp import HttpStatus


class LockedTokenError(HttpStatus):
    status_code, status_text, info = 462, 'Token is locked', 'The max try limitation is exceeded.'


class DeactivatedTokenError(HttpStatus):
    status_code, status_text, info = 463, 'Token is deactivated', 'Requested token is already deactivated.'


class DeviceNotFoundError(HttpStatus):
    status_code, status_text, info = 464, 'Device Not Found', 'Requested device is found.'
