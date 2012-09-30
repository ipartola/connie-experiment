
from http import ConnieHTTPConnection, CachedDNSHTTPConnection
from httplib import HTTPConnection

from bench import run_experiment

def fetch(cls, host, port, timeout):
    http = cls(host, port, timeout=timeout)
    http.connect()

    http.request('GET', '/')
    resp = http.getresponse()
    resp.read()
    http.close()

def connie_fetch(host, port, timeout):
    fetch(ConnieHTTPConnection, host, port, timeout)

def cached_dns_fetch(host, port, timeout):
    fetch(CachedDNSHTTPConnection, host, port, timeout)

def plain_fetch(host, port, timeout):
    fetch(HTTPConnection, host, port, timeout)

def main():
    FUNCTIONS = [
        connie_fetch,
        cached_dns_fetch,
        plain_fetch,
    ]

    run_experiment(FUNCTIONS)

if __name__ == '__main__':
    main()
