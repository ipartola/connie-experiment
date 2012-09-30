
ROUNDS = 5
HOSTS = ['google.com', 'apple.com', 'yandex.ru', 'facebook.com', 'maps.google.com', 'google.cn',]

import time

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

