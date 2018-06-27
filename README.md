# Minimal HTTP Servers

Minimal working examples of concurrency patterns using sockets.

Reading these in order will give you an introduction to sockets as well as the following topics.

1. Blocking I/O
1. Threading
1. Thread pools
1. Event Loops
1. Coroutines

## Invocation

Try out the servers in the following order (they bind to all interfaces).

    $ ./single_threaded.py 80
    $ ./multi_threaded_gif.py 80
    $ ./multi_threaded.py 80
    $ ./multi_threaded_pool.py 80 100
    $ ./single_threaded_select.py 80
    $ ./gevent_coroutines.py 80

## Datatbase

The later servers depend on a PostgreSQL database with the user "root" having
access to a database "testdb". Instructions for initializing this database are
in response/__init__.py

Alternatively, you can modify any of the servers to serve an HTML file rather
than make database queries by replacing the following line

    client_sock.sendall(response.random_uuids())

with this

    client_sock.sendall(response.html_file_response('your_file.html'))

Also, remove this line

    response.init_db_pool()

Copyright 2018, Andrew Sauber
Released under the MIT License

