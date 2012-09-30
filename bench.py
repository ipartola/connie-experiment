
ROUNDS = 5
HOSTS = ['google.com', 'apple.com', 'yandex.ru', 'facebook.com', 'maps.google.com', 'google.cn',]

import time, random, socket

def measure(func, *args, **kwargs):
    s = time.time()
    func(*args, **kwargs)
    t = time.time() - s
    return t

def stats(times):
    total = sum(times)
    avg = total / len(times)
    stddev = sum( (x - avg)**2 for x in times )**0.5 / len(times)

    return len(times), total, avg, stddev

def run_experiment(functions):
    for func in functions:
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

