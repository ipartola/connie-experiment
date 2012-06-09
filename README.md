
# Connie experiment

This project is an experimental implementation of Python's httplib.HTTPConnection
which establishes connections concurrently instead of serially.

## Typical implementation

Normally, if your domain name resolves to multiple A records, you see something
like this:

  $ host google.com
  google.com has address 173.194.37.70
  google.com has address 173.194.37.67
  google.com has address 173.194.37.78
  google.com has address 173.194.37.73
  google.com has address 173.194.37.71
  google.com has address 173.194.37.66
  google.com has address 173.194.37.64
  google.com has address 173.194.37.72
  google.com has address 173.194.37.69
  google.com has address 173.194.37.68
  google.com has address 173.194.37.65
  google.com has IPv6 address 2607:f8b0:4002:802::1004
  ...

The order of addresses is typically randomized by your libc resolver.

When you try to download http://google.com/, your browser or HTTP client will
grab the first address and try to connect to it. If the connection fails, it
will try the next one, but this happens after a long timeout.

## Connie's way

In an attempt to speed this up, Connie's implementation tries to connect to
all the addresses at once, and then uses a select() call to determine which
connection succeeded. It then closes all other connections and continues
talking to the address that responded first.

There are several results that stem from this scheme. First, if one of the
servers is down it will never be blindly selected as before. Second, we can bet
that the server to complete the TCP handshake first is likely also
geographically closer and faster than the rest.

Included with the project is bench.py which can be used to measure the effect
of using the httplib implementation vs the Connie one. Run it for yourself to
see the results.

## Prototype only

This code is prototype-only. For one, you'll run out of file descriptors
much more quickly with a scheme like this. For another, none of this has been
tested in production. In other words, feel free to use it for fun, but proceed
with caution when using for profit.
