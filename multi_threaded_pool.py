#!/usr/bin/env python3

import time
from metrics import count_request, time_request

import sock
import sys
from threading import Thread
from queue import Queue

import response

server_sock = sock.make_tcp_socket(int(sys.argv[1]))

q = Queue()

def http_thread():
    while True:
        client_sock = q.get()
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

threads = []
for _ in range(int(sys.argv[2])):
    t = Thread(target=http_thread)
    t.start()
    threads.append(t)

while True:
    try:
        client_sock, client_addr = server_sock.accept()
        q.put(client_sock)
    except:
        break
server_sock.close()

