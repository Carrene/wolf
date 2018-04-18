import sys

from restfulpy.cli import Launcher, RequireSubCommand

from .cryptoutil import EncryptedISOPinBlock, configuration_cipher


# noinspection PyAbstractClass
class PinBlockLauncher(Launcher, RequireSubCommand):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('pinblock', help='ISO-0 ANSI Pin Block tools')
        parser.add_argument('-k', '--key', help='The psk to (en/de)crypt.')
        parser.add_argument('-t', '--token-id', required=True, help='The token id')
        pinblock_subparsers = parser.add_subparsers(title="pinblock command", dest="pinblock_command")
        PinBlockEncodeLauncher.register(pinblock_subparsers)
        PinBlockDecodeLauncher.register(pinblock_subparsers)
        return parser


class PinBlockEncodeLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('encode', help='ISO-0 ANSI Pin Block encode')
        parser.add_argument('code', nargs='?', help='The code to encrypt. if omitted, the standard input will be used.')
        return parser

    def launch(self):
        code = self.args.code
        if not code:
            code = sys.stdin.read().strip()
        print(EncryptedISOPinBlock(self.args.token_id, key=self.args.key).encode(code).decode())


class PinBlockDecodeLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('decode', help='ISO-0 ANSI Pin Block decode')
        parser.add_argument('code', nargs='?', help='The code to decrypt. if omitted, the standard input will be used.')
        return parser

    def launch(self):
        code = self.args.code
        if not code:
            code = sys.stdin.read().strip()
        print(EncryptedISOPinBlock(self.args.token_id, key=self.args.key).decode(code).decode())


# noinspection PyAbstractClass
class ConfigLauncher(Launcher, RequireSubCommand):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('configuration', help='Configuration tools')
        subparsers = parser.add_subparsers(title="configuration command", dest="config_command")
        ConfigEncryptLauncher.register(subparsers)
        ConfigDecryptLauncher.register(subparsers)
        return parser


class ConfigEncryptLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('encrypt', help='Encrypt configu file')
        return parser

    def launch(self):
        sys.stdout.buffer.write(b'#enc')
        sys.stdout.buffer.write(configuration_cipher.encrypt(sys.stdin.buffer.read()))


class ConfigDecryptLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('decrypt', help='Decrypt the config file')
        return parser

    def launch(self):
        content = sys.stdin.buffer.read()
        if content[:4] == b'#enc':
            content = content[4:]
        sys.stdout.buffer.write(configuration_cipher.decrypt(content))

