
import time
from http import ConnieHTTPConnection
from httplib import HTTPConnection

from stats import measure, stats

def fetch(cls, host, port, path):
    http = cls(host, port, timeout=1.0)
    http.connect()

    http.request('GET', '/')
    resp = http.getresponse()
    resp.read()
    http.close()

def measure(func, *args, **kwargs):
    s = time.time()
    func(*args, **kwargs)
    return time.time() - s

def stats(times):
    total = sum(times)
    avg = total / len(times)
    stddev = sum( (x - avg)**2 for x in times )**0.5 / len(times)

    return total, avg, stddev

def main():
    ROUNDS = 10
    CLASSES = [ConnieHTTPConnection, HTTPConnection, ]
    HOSTS = ['google.com', 'apple.com', 'bing.com', 'yandex.ru', 'rambler.ru', 'narod.ru', 'maps.google.com', 'google.ca',]

    for cls in CLASSES:
        times = []
        for x in xrange(0, ROUNDS):
            for host in HOSTS:
                try:
                    times.append(measure(fetch, cls, host, 80, '/'))
                except Exception, e:
                    print e
        print cls.__name__, stats(times)

if __name__ == '__main__':
    main()
