from nanohttp import HTTPKnownStatus


class ExpiredTokenError(HTTPKnownStatus):
    status = '602 Token is expired'


class LockedTokenError(HTTPKnownStatus):
    status = '462 Token is locked'


class DeactivatedTokenError(HTTPKnownStatus):
    status = '603 Token is deactivated'

# FIXME: Rename it to key not found
class DeviceNotFoundError(HTTPKnownStatus):
    status = '464 Device Not Found'


class ActivatedTokenError(HTTPKnownStatus):
    status = '465 Token is active'


class NotLockedTokenError(HTTPKnownStatus):
    status = '466 Token is not locked'

