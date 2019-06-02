import socket
import threading
import binascii
import re
from datetime import date, timedelta

from nanohttp import settings
from restfulpy.cli import Launcher, RequireSubCommand
from restfulpy.orm import commit, DBSession
from iso8583.models import Envelope
from tlv import TLV

from .models import Token, Cryptomodule
from .exceptions import DeactivatedTokenError, ExpiredTokenError, \
    DuplicateSeedError, InvalidPartialCardNameError


worker_threads = {}


def worker(client_socket):
    length = client_socket.recv(4)
    message = length + client_socket.recv(int(length))
    mackey = binascii.unhexlify(settings.iso8583.mackey)
    envelope = Envelope.loads(message, mackey)

    TCP_server(envelope)

    envelope.mti = envelope.mti + 10
    response = envelope.dumps()

    client_socket.send(response)


def accept(client_socket):
    worker_thread = threading.Thread(
        target=worker,
        args=(client_socket,),
        daemon=True
    )
    worker_threads[client_socket.fileno] = worker
    worker_thread.start()


def listen(host, port):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    socket_server.listen(settings.tcpserver.backlog)

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

    def register(self, envelope):
        field48 = TLV.loads(envelope[48].value).fields

        token = self._find_or_create_token(
            envelope=envelope,
            phone=field48['PHN']
        )
        self._validate_token(token)

        DBSession.commit()
        field48['ACT'] = token.provision(field48['PHN']).split('/')[-1]
        envelope.set(39, b'000')
        tlv = TLV(**field48)
        envelope[48].value = tlv.dumps()

    def verify(self, envelope):
        raise NotImplementedError()

    _routes = {
        101: register,
        302: verify,
    }

    def _validate_token(self, token):
        if token.is_expired:
            raise ExpiredTokenError()

        if not token.is_active:
            raise DeactivatedTokenError()

    def _find_or_create_token(self, envelope, phone):
        partial_card_name = envelope[2].value.decode()
        cryptomodule_id = 1 if envelope[24].value[1] == 1 else 2
        bank_id = envelope[2].value[0:6].decode()
        pattern = settings.card_tokens[6].pattern
        if not re.match(pattern, partial_card_name):
            raise InvalidPartialCardNameError()

        if DBSession.query(Cryptomodule) \
                .filter(Cryptomodule.id == cryptomodule_id) \
                .count() <= 0:
            raise HTTPStatus(
                f'601 Cryptomodule does not exists: {cryptomodule_id}'
            )

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
            token.expire_date = date.today() + timedelta(days=1)
            token.seed = \
                b'\xdb!.\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
            token.cryptomodule_id = cryptomodule_id
            token.bank_id = 6
            token.name = partial_card_name
            token.is_active = True
            DBSession.add(token)

        token.initialize_seed()

        try:
            DBSession.flush()

        except IntegrityError as ex:
            raise DuplicateSeedError()

        else:
            return token


TCP_server = TCPServerController()

