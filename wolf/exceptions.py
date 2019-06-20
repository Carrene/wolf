from nanohttp import HTTPKnownStatus


class ExpiredTokenError(HTTPKnownStatus):
    status = '602 Token is expired'


class DeactivatedTokenError(HTTPKnownStatus):
    status = '603 Token is deactivated'


class DeviceNotFoundError(HTTPKnownStatus):
    status = '605 Device not found'

    def __init__(self, phone=None):
        if phone is not None:
            phone = f'Device is not found: {phone}'
        super().__init__(status_text=phone)


class SSMIsNotAvailableError(HTTPKnownStatus):
    status = '801 SSM is not available'


class SSMInternalError(HTTPKnownStatus):
    status = '802 SSM internal error'


class MaskanSendSmsError(HTTPKnownStatus):
    status = '803 Sms is not sending error'


class DuplicateSeedError(HTTPKnownStatus):
    status = '666 Cannot generate and randomize seed, please try again'


class InvalidPartialCardNameError(HTTPKnownStatus):
    status = '711 Invalid partial card name'

