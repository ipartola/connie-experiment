
import socket, select, time, random

from cache import Cache

TIMEOUT_FACTOR = 0.100
DNS_TTL = 60.0 # In seconds

cache = Cache(DNS_TTL)

def tuple_result(func):
    """Turns a generator into a function that returns a tuple

    Do not use on infinite generators."""

    def wrapper(*args, **kwargs):
        return tuple(func(*args, **kwargs))

    return wrapper

# We cache the result of this function to prevent DNS slowdowns from
# affecting the benchmark results
@cache.cached
@tuple_result
def _get_sockdefs(host, port, family, socktype, proto, flags):
    """Generator that yeilds tuples of (family, socktype, proto, canonname, sockaddr)"""

    addrs = socket.getaddrinfo(host, port, family, socktype, proto, flags)
    for sockdef in addrs:
        yield sockdef

def _make_sockets(sockdefs, source_addr):
    """Creates non-blocking sockets, one per address definition.

    Returns a list of not-yet-connected sockets.
    """

    errors = []
    result = []
    for family, socktype, proto, cannonname, sockaddr in sockdefs:
        s = socket.socket(family, socktype, proto)
        s.setblocking(0) # Do not block

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

        result.append(s)

    if len(errors) == len(sockdefs):
        e = Exception("Could not connect")
        e.errors = errors
        raise e

    return result
    
def _connect(host, port, conn_timeout, family=socket.AF_UNSPEC, socktype=socket.SOCK_STREAM, proto=0, flags=0, source_addr=None):
    """Internal connection function.

    This function accepts all possible options. It's return value is the
    socket that connected first.
    """

    sockdefs = _get_sockdefs(host, port, family, socktype, proto, flags)
    socks = _make_sockets(sockdefs, source_addr)
    
    socks_by_fd = dict((s.fileno(), s) for s in socks)

    sock = None
    ep = select.epoll()

    for s in socks:
        ep.register(s, select.EPOLLOUT)

    start_time = time.time()
    while not sock:
        if time.time() - start_time > conn_timeout:
            break

        w = ep.poll(timeout=conn_timeout, maxevents=1)
        if len(w) > 0:
            fd, event = w[0]
            if event == select.EPOLLOUT:
                sock = socks_by_fd[fd]

    if not sock:
        raise Exception('Could not connect: all %d attempted hosts timed out.' % len(socks))

    sock.setblocking(1)

    # Close all sockets that did not succeed
    [s.close() for s in socks if s != sock]

    return sock, sock.getpeername()

def connie_connect(host, port, timeout=None, source_addr=None):
    """Connects to the first connected socket."""

    sock, remote_addr = _connect(host, port, timeout, source_addr=source_addr)
    return sock

# We cache the result of this function to prevent DNS slowdowns from
# affecting the benchmark results
@cache.cached
def _get_random_addr(host, port):
    """Returns a random IP address for a given host."""

    socket.getaddrinfo(host, port)
    addrs = socket.getaddrinfo(host, port)
    return random.choice(addrs)[-1]

def cached_dns_connect(host, port, timeout, source_addr=None):
    """Performs a plain socket.connect to a random IP of the given (host, port).

    The DNS resolution of (host, port) is cached in memory.
    """

    addr = _get_random_addr(host, port)
    if len(addr) == 4:
        s = socket.socket(family=socket.AF_INET6)
    else:
        s = socket.socket(family=socket.AF_INET)

    if source_addr:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(source_addr)
        
    s.settimeout(timeout)
    s.connect(addr)
    return s

