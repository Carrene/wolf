from nanohttp import HTTPKnownStatus


class ExpiredTokenError(HTTPKnownStatus):
    status = '461 Token is expired'


class LockedTokenError(HTTPKnownStatus):
    status = '462 Token is locked'


class DeactivatedTokenError(HTTPKnownStatus):
    status = '463 Token is deactivated'


class DeviceNotFoundError(HTTPKnownStatus):
    status = '464 Device Not Found'


class ActivatedTokenError(HTTPKnownStatus):
    status = '465 Token is active'


class NotLockedTokenError(HTTPKnownStatus):
    status = '466 Token is not locked'

