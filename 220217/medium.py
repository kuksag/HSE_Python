from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime
import multiprocessing as mp
import functools
import logging
import math
import os

ARTIFACTS_DIR = 'artifacts'
LOG_NAME = 'medium.txt'
logging.basicConfig(filename=os.path.join(ARTIFACTS_DIR, LOG_NAME),
                    level=logging.DEBUG)


def log_integral(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info('Started function: {:>16}'.format(str(func.__name__)))
        logging.info('With args: {:>16}'.format(str(args)))

        start = datetime.now()
        result = func(*args, **kwargs)
        duration = datetime.now() - start

        logging.info('Got result: {:>32}'.format(result))
        logging.info('Finished with time: {:>16} mcs'.format(duration.microseconds))

        return result
    return wrapper


@log_integral
def integrate_with_threads(f, a, b, n_jobs=1, n_iter=1000):
    step = (b - a) / n_iter
    points = [a + i * step for i in range(n_iter)]
    with ThreadPoolExecutor(max_workers=n_jobs) as pool:
        result = pool.map(f, points)
    return step * sum(result)


@log_integral
def integrate_with_processes(f, a, b, n_jobs=1, n_iter=1000):
    step = (b - a) / n_iter
    points = [a + i * step for i in range(n_iter)]
    with ProcessPoolExecutor(max_workers=n_jobs) as pool:
        result = pool.map(f, points)
    return step * sum(result)


if __name__ == '__main__':
    for job in range(1, 2 * mp.cpu_count()):
        integrate_with_threads(math.cos, 0, math.pi / 2, job, 10000)
    for job in range(1, 2 * mp.cpu_count()):
        integrate_with_processes(math.cos, 0, math.pi / 2, job, 10000)
