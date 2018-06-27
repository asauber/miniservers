import os
import random
import psycopg2
import psycopg2.pool

def read_image_response_body():
    """Image response payload (cat gif)"""
    image_file = open(os.path.join(os.path.dirname(__file__), 'image.gif'), 'rb')
    return image_file.read()

def image_response(body):
    """Return an HTTP image/gif response from binary *body*"""
    payload = ("HTTP/1.1 200 OK\r\n"
               "Connection: keep-alive\r\n"
               "Content-Type: image/gif\r\n"
               "Content-Length: {}\r\n\r\n"
               "").format(len(body)).encode('utf-8') + body
    return payload

# static image payload for I/O saturation tests (cat gifs)
image_payload = image_response(read_image_response_body())

def text_response(body):
    """Return an HTTP text/plain response from binary *body*"""
    payload = ("HTTP/1.1 200 OK\r\n"
               "Connection: keep-alive\r\n"
               "Content-Type: text/plain\r\n"
               "Content-Length: {}\r\n\r\n"
               "").format(len(body)).encode('utf-8') + body
    return payload

def html_response(body):
    """Return an HTTP text/html response from binary *body*"""
    payload = ("HTTP/1.1 200 OK\r\n"
               "Connection: keep-alive\r\n"
               "Content-Type: text/html\r\n"
               "Content-Length: {}\r\n\r\n"
               "").format(len(body)).encode('utf-8') + body
    return payload

def file_response(filepath):
    """Return a text/plain response from *filepath*"""
    body = open(filepath, 'rb').read()
    return text_response(body)

def html_file_response(filepath):
    """Return a text/html response from *filepath*"""
    body = open(filepath, 'rb').read()
    return html_response(body)

def read_random_file_segment():
    """Read a random 512 byte segment of 'bigfile'"""
    # First, create "bigfile" in this module's directory
    # cat /dev/urandom > bigfile
    # kill it after 1 second or so
    filepath = os.path.join(os.path.dirname(__file__), 'bigfile')
    size = os.path.getsize(filepath)
    f = open(filepath, 'rb')
    f.seek(random.randint(0, max(0, size - 600)))
    seg = f.read(512)
    return seg

def random_from_file():
    """Return an HTTP response by reading a random segment of a big file"""
    body = read_random_file_segment()
    return text_response(body)

"""
PostgreSQL database 'testdb' initialized as follows:

create table t_random as select s, uuid_generate_v4() from generate_Series(1, 5000000) s;
create unique index on t_random (s);

This creates a table with 5,000,000 random UUIDs with autoincrement keys *s* which are indexed.
You must have the UUID extension installed from postgresql-contrib.
"""

"""Initialize a PostgreSQL connection pool with up to 10000 connections"""
dbpool = None
def init_db_pool():
    global dbpool
    dbpool = psycopg2.pool.ThreadedConnectionPool(1, 10000, "dbname=testdb user=root")

def query_random_uuids(conn):
    """Query for 10 random UUIDs by generating 10 random IDs locally"""
    cur = conn.cursor()
    cur.execute("""
        select uuid_generate_v4 from t_random
        where s in ({})
    """.format(", ".join([str(random.randint(1, 5000000)) for x in range(5)])))
    return ["".join(t) for t in cur.fetchall()]

def random_uuids():
    random_records = []
    conn = dbpool.getconn()
    for _ in range(5):
        random_records += query_random_uuids(conn)
    body = "\n".join(random_records).encode('utf-8')
    dbpool.putconn(conn)
    return text_response(body)

