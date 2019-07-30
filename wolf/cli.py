import sys
import time
import uuid
import binascii

from nanohttp import settings
from restfulpy.cli import Launcher, RequireSubCommand
from restfulpy.orm import DBSession
from oathcy.otp import TOTP

from wolf.cryptoutil import ISCPinBlock, PouyaPinBlock
from wolf.models import Token


class PinBlockLauncher(Launcher, RequireSubCommand):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'pinblock',
            help='ISO-0 ANSI Pin Block tools'
        )
        parser.add_argument('-k', '--key', help='The psk to (en/de)crypt.')
        parser.add_argument(
            '-t',
            '--token-id',
            required=True,
            help='The token id'
        )
        pinblock_subparsers = parser.add_subparsers(
            title='pinblock command',
            dest='pinblock_command'
        )
        PinBlockEncodeLauncher.register(pinblock_subparsers)
        PinBlockDecodeLauncher.register(pinblock_subparsers)
        return parser


class PinBlockEncodeLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'encode',
            help='ISO-0 ANSI Pin Block encode'
        )
        parser.add_argument(
            'code',
            nargs='?',
            help= \
                'The code to encrypt. if omitted, the standard input will be '
                'used.'
        )
        return parser

    def launch(self):  # pragma: no cover
        code = self.args.code
        if not code:
            code = sys.stdin.read().strip()

        tokenid = uuid.UUID(self.args.token_id) \
            if settings.pinblock.algorithm == 'isc' \
            else uuid.UUID(bytes=self.args.token_id.encode())

        token = DBSession.query(Token).get(tokenid)
        if not token:
            print(
                f'Token with id: {self.args.token_id} has not found',
                file=sys.stderr
            )
            return 1

        if settings.pinblock.algorithm == 'isc':
            pinblock = ISCPinBlock(token.id.bytes)

        else:
            pinblock = PouyaPinBlock(
                pan=f'6{self.args.token_id[1:]}'.encode(),
                key=binascii.unhexlify(settings.pinblock[8].key)
            )

        print(pinblock.encode(code).decode())


class PinBlockDecodeLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'decode', help=
            'ISO-0 ANSI Pin Block decode'
        )
        parser.add_argument(
            'code',
            nargs='?',
            help= \
                'The code to decrypt. if omitted, the standard input will be '
                'used.'
        )
        return parser

    def launch(self):  # pragma: no cover
        code = self.args.code
        if not code:
            code = sys.stdin.read().strip()

        tokenid = uuid.UUID(self.args.token_id) \
            if settings.pinblock.algorithm == 'isc' \
            else uuid.UUID(bytes=self.args.token_id.encode())

        token = DBSession.query(Token).get(tokenid)
        if not token:
            print(
                f'Token with id: {self.args.token_id} has not found',
                file=sys.stderr
            )
            return 1

        if settings.pinblock.algorithm == 'isc':
            pinblock = ISCPinBlock(token.id.bytes)

        else:
            pinblock = PouyaPinBlock(
                pan=f'6{self.args.token_id[1:]}'.encode(),
                key=binascii.unhexlify(settings.pinblock[8].key)
            )

        print(pinblock.decode(code).decode())


class OTPLauncher(Launcher, RequireSubCommand):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'otp',
            help='One time password utilities'
        )
        parser.add_argument(
            '-t',
            '--token-id',
            required=True,
            help='The token id'
        )
        parser.add_argument(
            '-u',
            '--unixtime',
            type=int,
            default=int(time.time()),
            help='Unix time.'
        )

        otp_subparsers = parser.add_subparsers(
            title='OTP commands',
            dest='otp_command'
        )
        OTPGenerateLauncher.register(otp_subparsers)
        OTPVerifyLauncher.register(otp_subparsers)
        return parser


class OTPGenerateLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'generate',
            help='Generate a new OTP'
        )
        return parser

    def launch(self):  # pragma: no cover
        if settings.pinblock.algorithm == 'isc':
            tokenid = uuid.UUID(self.args.token_id)

        else:
            tokenid = uuid.UUID(bytes=self.args.token_id.encode())

        token = DBSession.query(Token).get(tokenid)
        if token is None:
            print(
                f'Token with id: {self.args.token_id} was not found',
                file=sys.stderr
            )
            return 1

        print(TOTP(
            token.seed,
            self.args.unixtime,
            token.cryptomodule.one_time_password_length,
            step=token.cryptomodule.time_interval
        ).generate().decode())


class OTPVerifyLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'verify',
            help='Verify an OTP'
        )
        parser.add_argument(
            'otp',
            help='OTP to verify'
        )

        parser.add_argument(
            '-w',
            '--window',
            help='If not given, value will be grabed from configuraion ' \
                'infrastructure: oath.window'
        )

        return parser

    def launch(self):  # pragma: no cover
        token = DBSession.query(Token) \
            .filter(Token.id == self.args.token_id) \
            .one_or_none()

        if token is None:
            print(
                f'Token with id: {self.args.token_id} was not found',
                file=sys.stderr
            )
            return 1
        ok = TOTP(
            token.seed,
            self.args.unixtime,
            token.cryptomodule.one_time_password_length,
            step=token.cryptomodule.time_interval
        ).verify(
            self.args.otp.encode(),
            self.args.window if self.args.window
                 else settings.oath.window
        )

        if not ok:
            print('Invalid code', file=sys.stderr)
            return 1

