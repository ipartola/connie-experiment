
from connie import connect as _connie_connect
import socket

from stats import measure, stats

def plain_connect(host, port, timeout):
    s = socket.socket()
    s.settimeout(timeout)
    s.connect((host, port))
    s.close()

def connie_connect(host, port, timeout):
    s = _connie_connect(host, port, timeout)
    s.close()

def main():
    ROUNDS = 10
    FUNCTIONS = [connie_connect, plain_connect, ]
    HOSTS = ['google.com', 'apple.com', 'bing.com', 'yandex.ru', 'rambler.ru', 'narod.ru', 'maps.google.com', 'google.cn',]

    for func in FUNCTIONS:
        times = []
        for x in xrange(0, ROUNDS):
            for host in HOSTS:
                try:
                    times.append(measure(func, host, 80, 1.0))
                except Exception, e:
                    print e
        print func.__name__, stats(times)

if __name__ == '__main__':
    main()
