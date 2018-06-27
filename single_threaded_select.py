#!/usr/bin/env python3

import time
from metrics import count_request, time_request

import sock
import sys
import select

import response
response.init_db_pool()

server_sock = sock.make_tcp_socket(int(sys.argv[1]))

read_list = [server_sock]

def handle_server_read(s):
    client_sock, client_addr = s.accept()
    read_list.append(client_sock)

def handle_client_read(s):
    try:
        request = s.recv(512)
        # metrics
        start_time = time.time()

        if request:
            s.sendall(response.random_uuids())

            # metrics
            count_request()
            time_request(time.time() - start_time)
        else:
            s.close()
            read_list.remove(s)
    except:
        s.close()
        read_list.remove(s)

while True:
    try:
        readable_socks, _, _ = select.select(read_list, [], [])
        for s in readable_socks:
            if s is server_sock:
                handle_server_read(s)
            else:
                handle_client_read(s)
    except:
        break
server_sock.close()

