import sys

from restfulpy.cli import Launcher, RequireSubCommand

from .cryptoutil import ISO0PinBlock


# noinspection PyAbstractClass
class PinBlockLauncher(Launcher, RequireSubCommand):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('pinblock', help='ISO-0 ANSI Pin Block tools')
        pinblock_subparsers = parser.add_subparsers(title="admin command", dest="admin_command")
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
        print(ISO0PinBlock().encode(code))


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
        print(ISO0PinBlock().decode(code))
