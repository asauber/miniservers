#!/usr/bin/env python3

import sock
import sys

import response

server_sock = sock.make_tcp_socket(int(sys.argv[1]))

while True:
    try:
        client_sock, client_addr = server_sock.accept()
        while True:
            try:
                request = client_sock.recv(512)
                if request:
                    client_sock.sendall(response.image_payload)
                else:
                    break
            except:
                break
        client_sock.close()
    except:
        break
server_sock.close()

