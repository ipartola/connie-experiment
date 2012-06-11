
import socket, select, struct, time
        
l_onoff = 1
l_linger = 0
LINGER_OPT_VAL = struct.pack('ii', l_onoff, l_linger)
TIMEOUT_FACTOR = 0.100

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
    
def _timeout_func(i):
    return (i + 1) * TIMEOUT_FACTOR

def _connect(host, port, conn_timeout, family=socket.AF_UNSPEC, socktype=socket.SOCK_STREAM, proto=0, flags=0, source_addr=None):
    sockdefs = get_sockdefs(host, port, family, socktype, proto, flags)
    sock_addrs = make_sockets(sockdefs, source_addr)
    
    socks = sock_addrs.keys()
    socks_by_fd = dict((s.fileno(), s) for s in socks)

    sock, i = None, 0
    ep = select.epoll()

    for s in socks:
        ep.register(s, select.EPOLLOUT)

    start_time = time.time()
    while not sock:
        if time.time() - start_time > conn_timeout:
            break

        timeout = _timeout_func(i)
        w = ep.poll(timeout=timeout, maxevents=1)
        if len(w) > 0:
            fd, event = w[0]
            if event == select.EPOLLOUT:
                sock = socks_by_fd[fd]

    if not sock:
        raise Exception('Could not connect: all %d attempted hosts timed out.' % len(socks))

    sock.setblocking(1)
    [s.close() for s in socks if s != sock]
    return sock, sock_addrs[sock]

def connect(host, port, timeout=None, source_addr=None):
    sock, remote_addr = _connect(host, port, timeout, source_addr=source_addr)
    return sock

