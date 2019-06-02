import binascii
import socket

from iso8583.models import Envelope


REQUEST = \
    b'027111006030050008E100011662802314007513' \
    b'5966000076242719052313153821140121124410' \
    b'191431376242701111102000001111102   65\xc8\xc7' \
    b'\xe4\xdf \xe3\xd3\xdf\xe4             \xca\xe5' \
    b'\xd1\xc7\xe4        THRIR00' \
    b'00011234567890070212290073P13006762427CI' \
    b'F012111001209483PHN01109121902288TKT003S' \
    b'FTTOK003000TKR0020272CCB6661787BFE6'


MACKEY = binascii.unhexlify(b'1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C')


def test_iso8583_server(run_iso8583_server):
    host, port = run_iso8583_server()
    print(host, port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(REQUEST)
        length_message = client_socket.recv(4)
        message = length_message + client_socket.recv(int(length_message))

    envelope = Envelope.loads(message, MACKEY)

    assert envelope.mti == 1110
    assert envelope[2].value == b'6280231400751359'
    assert envelope[3].value == b'660000'
    assert envelope[11].value == b'762427'
    assert envelope[12].value == b'190523131538'
    assert envelope[22].value == b'211401211244'
    assert envelope[24].value == b'101'
    assert envelope[37].value == b'914313762427'
    assert envelope[41].value == b'01111102'
    assert envelope[42].value == b'000001111102   '
    assert envelope[48].value == b'P13006762427CIF012111001209483' \
        b'TKT003SFTTOK003000TKI00202ACT006123456'

    assert binascii.hexlify(envelope[64].value).decode().upper() \
        == '224590F5B84C1EE4'

