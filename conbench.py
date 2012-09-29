
from connie import connie_connect as _connie_connect, plain_connect as _plain_connect
import random

from stats import measure, stats
from bench import ROUNDS, HOSTS

def connie_connect(host, port, timeout):
    _connie_connect(host, port, timeout).close()

def plain_connect(host, port, timeout):
    _plain_connect(host, port, timeout).close()

def main():
    FUNCTIONS = (
        connie_connect,
        plain_connect,
    )

    for func in FUNCTIONS:
        times = []
        for x in xrange(0, ROUNDS):
            random.shuffle(HOSTS)
            for host in HOSTS:
                try:
                    times.append(measure(func, host, 80, 1.0))
                except Exception, e:
                    print e
        print '%s: total %0.4f, per call: %0.4f, std dev: %0.4f' % tuple([func.__name__] + list(stats(times)))

if __name__ == '__main__':
    main()

