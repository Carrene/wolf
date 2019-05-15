import socket
import threading

from restfulpy.cli import Launcher, RequireSubCommand


worker_threads = {}


def worker(client_socket):
    raise NotImplementedError()


def accept(client_socket):
    worker_thread = Threading.Thread(
        target=worker, args=client_socket, daemon=True
    )
    worker_threads[client_socket.fileno] = worker
    worker_thread.start()


def listen(host, port):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    socket_server.listen(1)

    client_connection, client_address = socket_server.accept()
    accept(client_connection)


DEFAULT_ADDRESS = '8088'


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
            default=DEFAULT_ADDRESS,
            help='Bind Address. default: %s' % DEFAULT_ADDRESS

        )
        return parser

    def launch(self):
        host, port = \
            self.args.bind.split(':') if ':' in self.args.bind \
            else ('', self.args.bind)

        print(f'Serving on {host}:{port}!!!')
        listen(host, port)

