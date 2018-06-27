import socket

# Allocate UDP socket for local collectd statsd plugin
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address_pair = ("localhost", 8125)

def count_request():
    """Send a count metric with a value of 1 """
    sock.sendto(b"request:1|c", address_pair)

def time_request(seconds):
    """Send a timer metric with a value of *seconds* seconds"""
    metric = "request_latency:{}|ms".format(str(seconds * 1000))
    sock.sendto(metric.encode('utf-8'), address_pair)

