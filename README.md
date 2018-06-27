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
in `response/__init__.py`

Alternatively, you can modify any of the servers to serve an HTML file rather
than make database queries by replacing the following line

    client_sock.sendall(response.random_uuids())

with this

    client_sock.sendall(response.html_file_response('your_file.html'))

While removing or commenting out this line

    response.init_db_pool()

## Notes

Clearly these are meant to be _minimal_ working examples. They demonstrate some
socket programming techniques, and some concurrency techniques.  For instance,
`single_threaded_select.py` can handle thousands of requests per second with
its concurrency technique and it's only about 50 lines long. Given this, there
are some things lacking in the code. Configuration could be done using a file,
`argparse` could be used for a help message. Bare exception handling could be
replace with something more fine-grained. The response loop for a client
connection could be turned into a decorator. The gevent version could be
re-written using Python 3 asyncio coroutines. Go wild! All of these
improvements, and more, can be done by you!

### Copyright

Copyright 2018, Andrew Sauber
Released under the MIT License

