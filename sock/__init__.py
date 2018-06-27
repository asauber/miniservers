import socket

def make_tcp_socket(port):
    """Get a TCP socket listening on *port*, setting address reuse options"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(('0.0.0.0', port))
    sock.listen()
    return sock
