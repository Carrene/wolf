import binascii
import re
import socket
import threading
from datetime import date, timedelta
import time

from iso8583.models import Envelope
from nanohttp import settings, LazyAttribute
from restfulpy.cli import Launcher, RequireSubCommand
from restfulpy.orm import DBSession
from restfulpy.logging_ import get_logger
from tlv import TLV
from khayyam import JalaliDatetime

from . import cryptoutil
from .exceptions import InvalidPartialCardNameError, DuplicateSeedError, \
    MaskanUsernamePasswordError, MaskanVersionNumberError, \
    MaskanSendSmsError, MaskanInvalidSessionIdError, \
    MaskanRepetitiousRequestNumberError, MaskanInvalidRequestTimeError, \
    MaskanInvalidDigitalSignatureError, MaskanUserNotPermitedError, \
    MaskanPersonNotFoundError, MaskanIncompleteParametersError, \
    MaskanMiscellaneousError

from .models import Token, MiniToken, Cryptomodule, Person
from wolf.authentication import MaskanAuthenticator
from wolf.backends import MaskanClient
from wolf.helpers import MaskanSmsProvider


logger = get_logger('ISO8583')
worker_threads = {}


ISO_STATUS_SUCCESS = b'000'
ISO_STATUS_INVALID_PASSWORD_OR_USERNAME = b'117'
ISO_STATUS_BLOCK_USER = b'106'
ISO_STATUS_TOKEN_NOT_FOUND = b'117'
ISO_STATUS_INTERNAL_ERROR = b'909'
ISO_STATUS_INVALID_CIF_OR_NATIONALCODE = b'145'
ISO_STATUS_INVALID_FORMAT_MESSAGE = b'928'
ISO_STATUS_NEED_TO_APPROVE_USER = b'303'
ISO_STATUS_MISMATCH_PHONENUMBER_IN_CIF = b'100'


ISO_FIELD_PAN = 2
ISO_FIELD_PROCESS_CODE = 3
ISO_FIELD_SYSTEM_TRACE_AUDIT_NUMBER = 11
ISO_FIELD_LOCAL_TRANSACTION_TIME = 12
ISO_FIELD_MERCHANT_TYPE = 18
ISO_FIELD_CONDITION_CODE = 22
ISO_FIELD_FUNCTION_CODE = 24
ISO_FIELD_CAPTURE_CODE = 26
ISO_FIELD_RETRIEVAL_REFERENCE_NUMBER = 37
ISO_FIELD_RESPONCE_CODE = 39
ISO_FIELD_TERMINAL_ID = 41
ISO_FIELD_MERCHANT_ID = 42
ISO_FIELD_TERMINAL_LOCALTION = 43
ISO_FIELD_ADDITIONAL_DATA = 48
ISO_FIELD_PIN_BLOCK = 52
ISO_FIELD_MAC = 64


def worker(client_socket):
    mackey = binascii.unhexlify(settings.iso8583.mackey)
    try:
        length = client_socket.recv(4)
        message = length + client_socket.recv(int(length))
        logger.info(f'ISO message received: {message}')
        mackey = binascii.unhexlify(settings.iso8583.mackey)
        envelope = Envelope.loads(message, mackey)
        TCP_server(envelope)
        envelope.mti = envelope.mti + 10

    except:
        envelope = Envelope('1110', mackey)
        envelope.set(ISO_FIELD_RESPONCE_CODE, ISO_STATUS_INTERNAL_ERROR)

    finally:
        response = envelope.dumps()
        client_socket.send(response)
        client_socket.close()

        DBSession.close()


def accept(client_socket):
    worker_thread = threading.Thread(
        target=worker,
        args=(client_socket,),
        daemon=True
    )
    worker_threads[client_socket.fileno] = worker
    worker_thread.start()


def listen(host, port, ready=None):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    socket_server.listen(settings.tcpserver.backlog)

    time.sleep(.3)
    if ready:
        ready.set()

    while True:
        client_connection, client_address = socket_server.accept()
        accept(client_connection)


DEFAULT_ADDRESS = 8088


class ISO8583Launcher(Launcher, RequireSubCommand):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'iso8583',
            help='ISO 8583 utilities'
        )
        iso8583_subparsers = parser.add_subparsers(
            title='iso8583 command',
            dest='iso8583_command'
        )
        ISO8583ServeLauncher.register(iso8583_subparsers)
        return parser


class ISO8583ServeLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'serve',
            help='Serve the ISO8583 tcp server'
        )
        parser.add_argument(
            '-b',
            '--bind',
            type=int,
            default=DEFAULT_ADDRESS,
            help='Bind Address. default: %s' % DEFAULT_ADDRESS

        )
        return parser

    def launch(self): # pragma: no cover
        host, port = \
            self.args.bind.split(':') if ':' in str(self.args.bind) \
            else ('', self.args.bind)

        print(f'Serving on {host}:{port}!!!')
        listen(host, port)


class TCPServerController:

    def __call__(self, envelope):
        function_code = int(envelope[ISO_FIELD_FUNCTION_CODE].value.decode())
        handler = self._routes.get(function_code)
        if handler is None:
            # FIXME: log
            envelope.set(
                ISO_FIELD_RESPONCE_CODE,
                ISO_STATUS_INVALID_FORMAT_MESSAGE
            )
            return envelope

        handler(self, envelope)

    @LazyAttribute
    def window(self):
        return settings.oath.window

    def _is_registeration_fields_valid(self, envelope):
        if ISO_FIELD_PAN not in envelope \
                or ISO_FIELD_ADDITIONAL_DATA not in envelope \
                or ISO_FIELD_FUNCTION_CODE not in envelope:
            return False

        field48 = TLV.loads(envelope[ISO_FIELD_ADDITIONAL_DATA].value).fields
        if 'PHN' not in field48:
            return False

        card_number = envelope[ISO_FIELD_PAN].value.decode()
        if not re.match(settings.card_tokens[6].pattern, card_number):
            return False

        return True

    def register(self, envelope):
        if not self._is_registeration_fields_valid(envelope):
            envelope.set(
                ISO_FIELD_RESPONCE_CODE,
                ISO_STATUS_INVALID_FORMAT_MESSAGE
            )
            return

        field48 = TLV.loads(envelope[ISO_FIELD_ADDITIONAL_DATA].value).fields
        phone = field48['PHN']
        customer_code = field48['CIF']

        person = Person()
        DBSession.add(person)
        DBSession.flush()
        request_number = person.id

        datetime = JalaliDatetime.now()

        def zero_padding_datetime(value):
            if len(str(value)) < 2:
                return f'0{value}'

            return value

        year = f'{datetime.year}'
        month = zero_padding_datetime(datetime.month)
        day = zero_padding_datetime(datetime.day)
        hour = zero_padding_datetime(datetime.hour)
        minute = zero_padding_datetime(datetime.minute)
        second = zero_padding_datetime(datetime.second)

        request_time = \
            f'{year}/{month}/{day} {hour}:{minute}:{second}'

        try:
            session_id = MaskanAuthenticator().login()

        except (MaskanUsernamePasswordError, MaskanVersionNumberError) as ex:
            logger.exception(ex)
            envelop.set(ISO_FIELD_RESPONCE_CODE, ISO_STATUS_INTERNAL_ERROR)
            return

        signature_message = \
            f'<CUSTOMERCODE><{customer_code}>' \
            f'<REQUESTNUMBER><{request_number}>' \
            f'<REQUESTTIME><{request_time}>' \
            f'<SESSIONID><{session_id}>'

        key_filename = settings.maskan_web_service.person_info.key_filename

        signature = cryptoutil.create_signature(
            key_filename=key_filename,
            message=signature_message,
            hash_algorithm='sha1'
        )

        try:
            person_information = MaskanClient().get_person_info(
                customer_code=customer_code,
                session_id=session_id,
                signature=signature,
                datetime=request_time,
                request_number=request_number
            )

        except (
            MaskanInvalidSessionIdError,
            MaskanRepetitiousRequestNumberError,
            MaskanInvalidRequestTimeError,
            MaskanInvalidDigitalSignatureError,
            MaskanUserNotPermitedError,
            MaskanPersonNotFoundError,
            MaskanIncompleteParametersError,
            MaskanMiscellaneousError
        ) as ex:

            logger.exception(ex)
            DBSession.commit()
            envelope.set(ISO_FIELD_RESPONCE_CODE, ISO_STATUS_INTERNAL_ERROR)
            return

        if person_information['mobile'] != phone:
            envelope.set(
                ISO_FIELD_RESPONCE_CODE,
                ISO_STATUS_MISMATCH_PHONENUMBER_IN_CIF
            )
            return

        person.customer_code = person_information['customer_code']
        person.national_id = person_information['national_id']
        person.name = person_information['name']
        person.family = person_information['family']
        person.mobile = person_information['mobile']
        DBSession.commit()

        partial_card_name = envelope[ISO_FIELD_PAN].value.decode()
        cryptomodule_id = 1 \
            if envelope[ISO_FIELD_FUNCTION_CODE].value[1] == 1 else 2
        bank_id = envelope[ISO_FIELD_PAN].value[0:6].decode()

        if DBSession.query(Cryptomodule) \
                .filter(Cryptomodule.id == cryptomodule_id) \
                .count() <= 0:
            # Cryptomodule does not exists
            envelope.set(
                ISO_FIELD_RESPONCE_CODE,
                ISO_STATUS_INTERNAL_ERROR
            )
            return

        token = DBSession.query(Token).filter(
            Token.name == partial_card_name,
            Token.cryptomodule_id == cryptomodule_id,
            Token.phone == phone,
            Token.bank_id == bank_id
        ).one_or_none()

        if token is None:
            # Creating a new token
            token = Token()
            token.phone = int(phone)
            token.expire_date = date.today() + timedelta(days=18250)
            token.cryptomodule_id = cryptomodule_id
            token.bank_id = 6
            token.name = partial_card_name
            token.is_active = True
            DBSession.add(token)

        try:
            token.initialize_seed(max_retry=2)

        except DuplicateSeedError as ex:
            logger.exception(ex)
            envelope.set(ISO_FIELD_RESPONCE_CODE, ISO_STATUS_INTERNAL_ERROR)
            return

        DBSession.commit()

        provision = token.provision(phone).split('/')[-1]
        try:
            sms_response = MaskanSmsProvider().send(
                phone,
                provision[:120]
            )

        except MaskanSendSmsError as ex:
            logger.exception(ex)
            envelope.set(ISO_FIELD_RESPONCE_CODE, ISO_STATUS_INTERNAL_ERROR)
            return

        field48['ACT'] = provision[-8:]
        envelope.set(ISO_FIELD_RESPONCE_CODE, ISO_STATUS_SUCCESS)
        tlv = TLV(**field48)
        envelope[ISO_FIELD_ADDITIONAL_DATA].value = tlv.dumps()

    def verify(self, envelope):
        primitive = 'no'
        pinblock = envelope[ISO_FIELD_PIN_BLOCK].value
        envelope.unset(ISO_FIELD_PIN_BLOCK)
        token = DBSession.query(Token) \
            .filter(Token.name == envelope[ISO_FIELD_PAN].value.decode()) \
            .one_or_none()
        if token is None:
            envelope.set(ISO_FIELD_RESPONCE_CODE, ISO_STATUS_TOKEN_NOT_FOUND)
            return

        if not token.is_active:
            envelope.set(ISO_FIELD_RESPONCE_CODE, ISO_STATUS_BLOCK_USER)
            return

        token = MiniToken.load(token.id, cache=settings.token.redis.enabled)
        if token is None:
            envelope.set(ISO_FIELD_RESPONCE_CODE, ISO_STATUS_TOKEN_NOT_FOUND)
            return

        try:
            is_valid = token.verify(pinblock, self.window, primitive=primitive)
            token.cache()

        except ValueError:
            is_valid = False

        if not is_valid:
            envelope.set(
                ISO_FIELD_RESPONCE_CODE,
                ISO_STATUS_INVALID_PASSWORD_OR_USERNAME
            )
            return

        envelope.set(
            ISO_FIELD_RESPONCE_CODE,
            ISO_STATUS_SUCCESS
        )


    _routes = {
        101: register,
        302: verify,
    }


TCP_server = TCPServerController()


