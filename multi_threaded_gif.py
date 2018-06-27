#!/usr/bin/env python3

import time
from metrics import count_request, time_request

import sock
import sys
import _thread

import response

server_sock = sock.make_tcp_socket(int(sys.argv[1]))

def http_thread(client_sock):
    while True:
        try:
            request = client_sock.recv(512)
            # metrics
            start_time = time.time()

            if request:
                client_sock.sendall(response.image_payload)

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
        _thread.start_new_thread(http_thread, (client_sock,))
    except:
        break
server_sock.close()

