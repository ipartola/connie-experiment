
import socket, select, httplib, struct
        
l_onoff = 1
l_linger = 0
LINGER_OPT_VAL = struct.pack('ii', l_onoff, l_linger)

def tuple_result(func):
    def wrapper(*args, **kwargs):
        return tuple(func(*args, **kwargs))

    return wrapper

@tuple_result
def get_sockdefs(host, port, family, socktype, proto, flags):
    addrs = socket.getaddrinfo(host, port, family, socktype, proto, flags)
    for sockdef in addrs:
        yield sockdef

def make_sockets(sockdefs, source_addr):
    errors = []
    result = {}
    for family, socktype, proto, cannonname, sockaddr in sockdefs:
        s = socket.socket(family, socktype, proto)
        s.setblocking(0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, LINGER_OPT_VAL)

        if source_addr:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(source_addr)
        
        try:
            s.connect(sockaddr)
        except socket.error, e:
            if e.errno == 115:
                # Operation in progress means we are non-blocking. Ignore it.
                pass
            else:
                errors.append(e)
                continue

        result[s] = sockaddr

    if len(errors) == len(sockdefs):
        e = Exception("Could not connect")
        e.errors = errors
        raise e

    return result

def connect(host, port, conn_timeout, io_timeout, family=socket.AF_UNSPEC, socktype=socket.SOCK_STREAM, proto=0, flags=0, source_addr=None):
    sockdefs = get_sockdefs(host, port, family, socktype, proto, flags)
    sock_addrs = make_sockets(sockdefs, source_addr)
    
    socks = sock_addrs.keys()

    r, w, e = select.select(socks, socks, socks, conn_timeout)
    if len(w) < 1:
        raise Exception('Could not connect: all %d attempted hosts timed out.' % len(socks))

    sock = w[0]
    sock.setblocking(1)
    sock.settimeout(io_timeout)
    [s.close() for s in socks if s != sock]
    return sock, sock_addrs[sock]

class ConnieHTTPConnection(httplib.HTTPConnection):

    def connect(self):
        self.sock, remote_addr = connect(self.host, self.port,
            self.timeout, self.timeout, source_addr=self.source_address)

        if self._tunnel_host:
            self._tunnel()

if __name__ == '__main__':
    http = ConnieHTTPConnection('narod.ru', 80, timeout=1.0)
    http.connect()

    http.request('GET', '/')
    resp = http.getresponse()
    print resp.read()

