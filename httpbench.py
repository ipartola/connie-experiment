
from http import ConnieHTTPConnection, CachedDNSHTTPConnection
from httplib import HTTPConnection

from bench import ROUNDS, HOSTS, measure, stats
import random, socket

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
        CachedDNSHTTPConnection,
        HTTPConnection,
    ]

    for cls in CLASSES:
        times = []
        x = 0
        while x < ROUNDS*len(HOSTS):
            host = random.choice(HOSTS)
            try:
                times.append(measure(fetch, cls, host, 80, '/'))
                x += 1
            except socket.error, e:
                if e.errno == 101:
                    pass # Network unreachable could be due to lack of IPv6. Ignore it, but only in benchmarks
                else:
                    print e
            except Exception, e:
                print e
        print '%s: count %d, total %0.4f, per call: %0.4f, std dev: %0.4f' % tuple([cls.__name__] + list(stats(times)))

if __name__ == '__main__':
    main()
