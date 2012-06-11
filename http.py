
import httplib
from connie import connect

class ConnieHTTPConnection(httplib.HTTPConnection):

    def connect(self):
        self.sock = connect(self.host, self.port, self.timeout, self.source_address)

        if self._tunnel_host:
            self._tunnel()

if __name__ == '__main__':
    http = ConnieHTTPConnection('narod.ru', 80, timeout=1.0)
    http.connect()

    http.request('GET', '/')
    resp = http.getresponse()
    print resp.read()

