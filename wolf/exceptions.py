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


class MaskanUsernamePasswordError(HTTPKnownStatus):
    status = '804 Invalid username or password'


class MaskanVersionNumberError(HTTPKnownStatus):
    status = '805 Version number error'


class MaskanInvalidSessionIdError(HTTPKnownStatus):
    status = '806 Invalid or expired seeesion id'


class MaskanRepetitiousRequestNumberError(HTTPKnownStatus):
    status = '807 Repetitious request number'


class MaskanInvalidRequestTimeError(HTTPKnownStatus):
    status = '808 Invalid request time'


class MaskanInvalidDigitalError(HTTPKnownStatus):
    status = '809 Invalid digital signature'


class MaskanUserNotPermitedError(HTTPKnownStatus):
    status = '810 Not permited error'


class MaskanPersonNotFoundError(HTTPKnownStatus):
    status = '811 Person not found error'


class MaskanIncompleteParametersError(HTTPKnownStatus):
    status = '812 Incompleted parameters error'


class MaskanMiscellaneousError(HTTPKnownStatus):
    status = '813 Miscellaneous error'


class DuplicateSeedError(HTTPKnownStatus):
    status = '666 Cannot generate and randomize seed, please try again'


class InvalidPartialCardNameError(HTTPKnownStatus):
    status = '711 Invalid partial card name'

