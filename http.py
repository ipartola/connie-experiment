
import httplib
from connie import connie_connect

class ConnieHTTPConnection(httplib.HTTPConnection):
    """An HTTP Connectoin class that uses connie_connect."""

    def connect(self):
        self.sock = connie_connect(self.host, self.port, self.timeout, self.source_address)

        if self._tunnel_host:
            self._tunnel()

if __name__ == '__main__':
    http = ConnieHTTPConnection('www.google.com', 80, timeout=1.0)
    http.connect()

    http.request('GET', '/')
    resp = http.getresponse()
    print resp.read()

