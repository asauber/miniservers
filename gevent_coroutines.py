#!/usr/bin/env python3

import gevent.monkey
gevent.monkey.patch_all()

import time
from metrics import count_request, time_request

import sock
import sys
import gevent

import response

server_sock = sock.make_tcp_socket(int(sys.argv[1]))

def http_coroutine(client_sock):
    while True:
        try:
            request = client_sock.recv(512)
            # metrics
            start_time = time.time()

            if request:
                client_sock.sendall(response.random_uuids())

                # metrics
                count_request()
                time_request(time.time() - start_time)
            else:
                break
        except:
            break
    client_sock.close()

while True:
    try:
        client_sock, client_addr = server_sock.accept()
        gevent.spawn(http_coroutine, client_sock)
    except:
        break
server_sock.close()

