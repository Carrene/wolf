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
from tlv import TLV

from .exceptions import InvalidPartialCardNameError
from .models import Token, MiniToken, Cryptomodule


worker_threads = {}


def worker(client_socket):
    try:
        length = client_socket.recv(4)
        message = length + client_socket.recv(int(length))
        mackey = binascii.unhexlify(settings.iso8583.mackey)
        envelope = Envelope.loads(message, mackey)

        TCP_server(envelope)

        envelope.mti = envelope.mti + 10
        response = envelope.dumps()

        client_socket.send(response)
        client_socket.close()
    finally:
        DBSession.close()


def accept(client_socket):
    worker_thread = threading.Thread(
        target=worker,
        args=(client_socket,),
        daemon=True
    )
    worker_threads[client_socket.fileno] = worker
    worker_thread.start()


def listen(host, port, ready):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    socket_server.listen(settings.tcpserver.backlog)

    time.sleep(.3)
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

    def launch(self):
        host, port = \
            self.args.bind.split(':') if ':' in str(self.args.bind) \
            else ('', self.args.bind)

        print(f'Serving on {host}:{port}!!!')
        listen(host, port)


class TCPServerController:

    def __call__(self, envelope):
        function_code = int(envelope[24].value.decode())
        handler = self._routes.get(function_code)
        if handler is None:
            # FIXME: log
            envelope.set(39, b'928')
            return envelope

        handler(self, envelope)

    @LazyAttribute
    def window(self):
        return settings.oath.window

    def _is_registeration_fields_valid(self, envelope):
        if 2 not in envelope or 48 not in envelope or 24 not in envelope:
            return False

        field48 = TLV.loads(envelope[48].value).fields
        if 'PHN' not in field48:
            return False

        if not re.match(
            settings.card_tokens[6].pattern,
            envelope[2].value.decode()
        ):
            return False

        return True

    def register(self, envelope):
        if not self._is_registeration_fields_valid(envelope):
            # Invalid message format
            envelope.set(39, b'928')
            return

        field48 = TLV.loads(envelope[48].value).fields
        phone = field48['PHN']
        partial_card_name = envelope[2].value.decode()
        cryptomodule_id = 1 if envelope[24].value[1] == 1 else 2
        bank_id = envelope[2].value[0:6].decode()
        if DBSession.query(Cryptomodule) \
                .filter(Cryptomodule.id == cryptomodule_id) \
                .count() <= 0:
            # Cryptomodule does not exists
            envelope.set(39, b'909') # Internal error (DuplicateSeedError).
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
            token.expire_date = date.today() + timedelta(days=365)
            token.cryptomodule_id = cryptomodule_id
            token.bank_id = 6
            token.name = partial_card_name
            token.is_active = True
            DBSession.add(token)

        token.initialize_seed()

        try:
            DBSession.flush()

        except IntegrityError as ex:
            # Internal error (DuplicateSeedError).
            envelope.set(39, b'909')
            return

        if not token.is_active:
            # User is blocked.
            envelope.set(39, b'106')
            return

        if token.is_expired:
            # TODO: Set related response code.
            pass

        DBSession.commit()
        field48['ACT'] = token.provision(field48['PHN']).split('/')[-1]
        envelope.set(39, b'000') # Response is ok
        tlv = TLV(**field48)
        envelope[48].value = tlv.dumps()

    def verify(self, envelope):
        primitive = 'yes'
        pinblock = envelope[52].value
        envelope.unset(52)
        token = DBSession.query(Token) \
            .filter(Token.name == envelope[2].value.decode()) \
            .one_or_none()
        if token is None:
            envelope.set(39, b'117') # Token not found.
            return

        if not token.is_active:
            envelope.set(39, b'106') # User is blocked.
            return

        if token.is_expired:
            # TODO: Set related response code.
            pass

        token = MiniToken.load(token.id, cache=settings.token.redis.enabled)
        if token is None:
            envelope.set(39, b'117')
            return

        try:
            is_valid = token.verify(
                pinblock,
                self.window,
                primitive=primitive
            )
            token.cache()
        except ValueError:
            is_valid = False

        if not is_valid:
            envelope.set(39, b'117') # Incorecct the username or password.
            return

        envelope.set(39, b'000') # Respose is ok.


    _routes = {
        101: register,
        302: verify,
    }


TCP_server = TCPServerController()

