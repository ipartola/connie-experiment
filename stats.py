
import time

def measure(func, *args, **kwargs):
    s = time.time()
    func(*args, **kwargs)
    return time.time() - s

def stats(times):
    total = sum(times)
    avg = total / len(times)
    stddev = sum( (x - avg)**2 for x in times )**0.5 / len(times)

    return total, avg, stddev

