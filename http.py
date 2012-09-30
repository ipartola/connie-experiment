
import httplib
from connie import connie_connect, cached_dns_connect

class CachedDNSHTTPConnection(httplib.HTTPConnection):
    """An HTTP Connectoin class that uses connie_connect."""

    def connect(self):
        self.sock = cached_dns_connect(self.host, self.port, self.timeout, getattr(self, 'source_address', None))

        if self._tunnel_host:
            self._tunnel()

class ConnieHTTPConnection(httplib.HTTPConnection):
    """An HTTP Connectoin class that uses connie_connect."""

    def connect(self):
        self.sock = connie_connect(self.host, self.port, self.timeout, getattr(self, 'source_address', None))

        if self._tunnel_host:
            self._tunnel()

if __name__ == '__main__':
    http = ConnieHTTPConnection('www.google.com', 80, timeout=1.0)
    http.connect()

    http.request('GET', '/')
    resp = http.getresponse()
    print resp.read()

