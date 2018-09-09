from nanohttp import HTTPKnownStatus


class ExpiredTokenError(HTTPKnownStatus):
    status = '602 Token is expired'

class DeactivatedTokenError(HTTPKnownStatus):
    status = '603 Token is deactivated'

# FIXME: Rename it to key not found
class DeviceNotFoundError(HTTPKnownStatus):
    status = '464 Device Not Found'

