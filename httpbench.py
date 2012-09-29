
from http import ConnieHTTPConnection
from httplib import HTTPConnection

from stats import measure, stats
from bench import ROUNDS, HOSTS
import random

def fetch(cls, host, port, path):
    http = cls(host, port, timeout=1.0)
    http.connect()

    http.request('GET', '/')
    resp = http.getresponse()
    resp.read()
    http.close()

def main():
    CLASSES = [
        ConnieHTTPConnection,
        HTTPConnection,
    ]

    for cls in CLASSES:
        times = []
        for x in xrange(0, ROUNDS):
            random.shuffle(HOSTS)
            for host in HOSTS:
                try:
                    times.append(measure(fetch, cls, host, 80, '/'))
                except Exception, e:
                    print e
        print '%s: total %0.4f, per call: %0.4f, std dev: %0.4f' % tuple([cls.__name__] + list(stats(times)))

if __name__ == '__main__':
    main()
