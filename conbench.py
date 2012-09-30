
from connie import connie_connect as _connie_connect, cached_dns_connect as _cached_dns_connect
import random, socket

from bench import ROUNDS, HOSTS, measure, stats

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

    for func in FUNCTIONS:
        times = []
        x = 0
        while x < ROUNDS*len(HOSTS):
            host = random.choice(HOSTS)
            try:
                times.append(measure(func, host, 80, 1.0))
                x += 1
            except socket.error, e:
                if e.errno == 101:
                    pass # Network unreachable could be due to lack of IPv6. Ignore it, but only in benchmarks
                else:
                    print e
            except Exception, e:
                print e
        print '%20s: count %d, total %0.4f, per call: %0.4f, std dev: %0.4f' % tuple([func.__name__] + list(stats(times)))

if __name__ == '__main__':
    main()

