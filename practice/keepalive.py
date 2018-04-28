#! /usr/bin/env python3

import socket

HOST = '192.168.1.96'
PORT = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for i in range(10):
        s.sendall(
            b'VERIFY /apiv1/tokens/' + str(i).encode() + b'/codes/234234234 HTTP/1.1\n'
            b'Host: 192.168.1.96\n'
            b'Connection: keep-alive\n\n'
        )
        data = s.recv(1024)
        print('#' * 23)
        print('Received', repr(data))

