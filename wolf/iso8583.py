import binascii
import re
import socket
import threading
import time
import traceback
from datetime import date, timedelta

from iso8583.models import Envelope
from khayyam import JalaliDatetime
from nanohttp import settings, LazyAttribute, HTTPKnownStatus
from restfulpy.cli import Launcher, RequireSubCommand
from restfulpy.logging_ import get_logger
from restfulpy.orm import DBSession
from tlv import TLV

from . import cryptoutil
from .exceptions import DuplicateSeedError
from .models import Token, MiniToken, MaskanMiniToken, Cryptomodule, Person
from wolf.authentication import MaskanAuthenticator
from wolf.backends import MaskanClient
from wolf.helpers import MaskanSmsProvider


logger = get_logger('ISO8583')
worker_threads = {}


MASKAN_BANK_ID = 8


ISOSTATUS_SUCCESS = b'000'
ISOSTATUS_INVALID_PASSWORD_OR_USERNAME = b'117'
ISOSTATUS_BLOCK_USER = b'106'
ISOSTATUS_TOKEN_NOT_FOUND = b'117'
ISOSTATUS_INTERNAL_ERROR = b'909'
ISOSTATUS_INVALID_CIF_OR_NATIONALCODE = b'145'
ISOSTATUS_INVALID_FORMAT_MESSAGE = b'928'
ISOSTATUS_NEED_TO_APPROVE_USER = b'303'
ISOSTATUS_MISMATCH_PHONENUMBER_IN_CIF = b'100'


ISOFIELD_PAN = 2
ISOFIELD_PROCESS_CODE = 3
ISOFIELD_SYSTEM_TRACE_AUDIT_NUMBER = 11
ISOFIELD_LOCAL_TRANSACTION_TIME = 12
ISOFIELD_MERCHANT_TYPE = 18
ISOFIELD_CONDITION_CODE = 22
ISOFIELD_FUNCTION_CODE = 24
ISOFIELD_CAPTURE_CODE = 26
ISOFIELD_RETRIEVAL_REFERENCE_NUMBER = 37
ISOFIELD_RESPONSECODE = 39
ISOFIELD_TERMINAL_ID = 41
ISOFIELD_MERCHANT_ID = 42
ISOFIELD_TERMINAL_LOCALTION = 43
ISOFIELD_ADDITIONAL_DATA = 48
ISOFIELD_PIN_BLOCK = 52
ISOFIELD_MAC = 64


def worker(client_socket):
    mackey = binascii.unhexlify(settings.iso8583.mackey)
    try:
        length = client_socket.recv(4)
        if not length.isdigit():
            logger.exception(f'Invalid message length type: {length}')
            envelope = Envelope('1110', mackey)
            envelope.set(
                ISOFIELD_RESPONSECODE,
                ISOSTATUS_INVALID_FORMAT_MESSAGE
            )
            return

        message = b''.join([length, client_socket.recv(int(length))])
        envelope = Envelope.loads(message, mackey)

    except Exception:
        logger.exception(
            f'Can\'t load message length {length} message {message}'
        )
        logger.exception(traceback.format_exc())
        envelope = Envelope('1110', mackey)
        envelope.set(ISOFIELD_RESPONSECODE, ISOSTATUS_INVALID_FORMAT_MESSAGE)

    else:
        try:
            iso8583_handler(envelope)
            envelope.mti = envelope.mti + 10

        except Exception:
            logger.exception(traceback.format_exc())
            envelope.set(ISOFIELD_RESPONSECODE, ISOSTATUS_INTERNAL_ERROR)

    finally:
        response_log = ''
        for field in envelope.elements:
            if envelope[field] is not None:
                response_log = f'{response_log}Field {field}: ' \
                    f"{envelope[field].value.decode('latin-1')} "

        logger.info(response_log)
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
        function_code = int(envelope[ISOFIELD_FUNCTION_CODE].value.decode())
        handler = self._routes.get(function_code)
        if handler is None:
            envelope.set(
                ISOFIELD_RESPONSECODE,
                ISOSTATUS_INVALID_FORMAT_MESSAGE
            )
            logger.exception(
                f'Function code with code {function_code} not found'
            )
            return envelope

        handler(self, envelope)

    @LazyAttribute
    def window(self):
        return settings.oath.window

    def _is_registeration_fields_valid(self, envelope):
        if ISOFIELD_PAN not in envelope \
                or ISOFIELD_ADDITIONAL_DATA not in envelope \
                or ISOFIELD_FUNCTION_CODE not in envelope:
            return False

        field48 = TLV.loads(envelope[ISOFIELD_ADDITIONAL_DATA].value).fields
        if 'PHN' not in field48:
            return False

        card_number = envelope[ISOFIELD_PAN].value.decode()
        if not re.match(
            settings.card_tokens[MASKAN_BANK_ID].pattern,
            card_number
        ):
            return False

        return True

    def register(self, envelope):
        if not self._is_registeration_fields_valid(envelope):
            envelope.set(
                ISOFIELD_RESPONSECODE,
                ISOSTATUS_INVALID_FORMAT_MESSAGE
            )
            return

        field48 = TLV.loads(envelope[ISOFIELD_ADDITIONAL_DATA].value).fields
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

        except HTTPKnownStatus:
            logger.exception(traceback.format_exc())
            envelop.set(ISOFIELD_RESPONSECODE, ISOSTATUS_INTERNAL_ERROR)
            return

        signature_message = \
            f'<CUSTOMERCODE><{customer_code}>' \
            f'<REQUESTNUMBER><{request_number}>' \
            f'<REQUESTTIME><{request_time}>' \
            f'<SESSIONID><{session_id}>'

        key_filename = settings.maskan_web_service.person_info.key_filename

        signature = cryptoutil.create_signature(
            key_filename=key_filename,
            message=signature_message.encode(),
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

        except HTTPKnownStatus:
            logger.exception(traceback.format_exc())
            DBSession.commit()
            envelope.set(ISOFIELD_RESPONSECODE, ISOSTATUS_INTERNAL_ERROR)
            return

        if person_information['mobile'][-10:] != phone[-10:]:
            envelope.set(
                ISOFIELD_RESPONSECODE,
                ISOSTATUS_MISMATCH_PHONENUMBER_IN_CIF
            )
            return

        person.customer_code = person_information['customer_code']
        person.national_id = person_information['national_id']
        person.name = person_information['name']
        person.family = person_information['family']
        person.mobile = person_information['mobile']
        DBSession.commit()

        cryptomodule_id = 1 \
            if envelope[ISOFIELD_FUNCTION_CODE].value[1] == 1 else 2
        pan = envelope[ISOFIELD_PAN].value.decode()
        bank_id = pan[0:6]

        if DBSession.query(Cryptomodule) \
                .filter(Cryptomodule.id == cryptomodule_id) \
                .count() <= 0:
            # Cryptomodule does not exists
            envelope.set(
                ISOFIELD_RESPONSECODE,
                ISOSTATUS_INTERNAL_ERROR
            )
            return

        token = DBSession.query(Token).filter(
            Token.name == pan,
            Token.cryptomodule_id == cryptomodule_id,
            Token.phone == phone,
            Token.bank_id == MASKAN_BANK_ID
        ).one_or_none()

        if token is None:
            # Creating a new token
            token = Token()
            token.phone = int(phone)
            token.expire_date = date.today() + timedelta(days=18250)
            token.cryptomodule_id = cryptomodule_id
            token.bank_id = MASKAN_BANK_ID
            token.name = pan
            token.is_active = True
            DBSession.add(token)

        try:
            token.initialize_seed(max_retry=2)

        except DuplicateSeedError as ex:
            logger.exception(traceback.format_exc())
            envelope.set(ISOFIELD_RESPONSECODE, ISOSTATUS_INTERNAL_ERROR)
            return

        DBSession.commit()

        try:
            from pudb import set_trace; set_trace()
            provision = token.provision(f'98{phone[-10:]}').split('/')[-1]
            sms_response = MaskanSmsProvider().send(
                phone,
                provision[:120]
            )

        except HTTPKnownStatus:
            logger.exception(traceback.format_exc())
            envelope.set(ISOFIELD_RESPONSECODE, ISOSTATUS_INTERNAL_ERROR)

        else:
            field48['ACT'] = provision[-8:]
            envelope.set(ISOFIELD_RESPONSECODE, ISOSTATUS_SUCCESS)
            tlv = TLV(**field48)
            envelope[ISOFIELD_ADDITIONAL_DATA].value = tlv.dumps()

    def verify(self, envelope):
        primitive = False
        pinblock = envelope[ISOFIELD_PIN_BLOCK].value
        envelope.unset(ISOFIELD_PIN_BLOCK)
        cryptomodule_id = 1 \
            if envelope[ISOFIELD_FUNCTION_CODE].value[1] == 1 else 2
        pan = envelope[ISOFIELD_PAN].value.decode()

        token = MaskanMiniToken.load(
            pan.encode(),
            cache=settings.token.redis.enabled
        )
        if token is None:
            envelope.set(ISOFIELD_RESPONSECODE, ISOSTATUS_TOKEN_NOT_FOUND)
            return

        if not token.is_active:
            envelope.set(ISOFIELD_RESPONSECODE, ISOSTATUS_BLOCK_USER)
            return

        try:
            is_valid = token.verify(
                pinblock,
                self.window,
                token.bank_id,
                pan=pan.encode(),
                primitive=primitive
            )
            token.cache(pan.encode())

        except ValueError:
            is_valid = False

        if not is_valid:
            envelope.set(
                ISOFIELD_RESPONSECODE,
                ISOSTATUS_INVALID_PASSWORD_OR_USERNAME
            )
            return

        envelope.set(ISOFIELD_RESPONSECODE, ISOSTATUS_SUCCESS)


    _routes = {
        101: register,
        302: verify,
    }


iso8583_handler = TCPServerController()

