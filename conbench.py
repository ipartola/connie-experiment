
from connie import connie_connect as _connie_connect, cached_dns_connect as _cached_dns_connect

import socket

from bench import run_experiment

def connie_connect(host, port, timeout):
    _connie_connect(host, port, timeout).close()

def cached_dns_connect(host, port, timeout):
    _cached_dns_connect(host, port, timeout).close()

def plain_connect(host, port, timeout):
    s = socket.socket()
    s.settimeout(timeout)
    s.connect((host, port))
    s.close()

def main():
    FUNCTIONS = (
        connie_connect,
        cached_dns_connect,
        plain_connect,
    )

    run_experiment(FUNCTIONS)

if __name__ == '__main__':
    main()

