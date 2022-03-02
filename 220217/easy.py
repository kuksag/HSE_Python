import itertools
from datetime import datetime
import multiprocessing as mp
import threading
import os

ARTIFACTS_DIR = 'artifacts'
RESULT = 'easy.txt'


def calc_time(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        return datetime.now() - start
    return wrapper


def calc_fib(n: int) -> list:
    result = [0, 1]
    while len(result) < n:
        result.append(result[-1] + result[-2])
    return result


@calc_time
def run_sequential(reps, *fib_args):
    for _ in range(reps):
        calc_fib(*fib_args)


@calc_time
def run_with_threads(reps, *fib_args):
    threads = [threading.Thread(target=calc_fib, args=(*fib_args, )) for _ in range(reps)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


@calc_time
def run_with_processes(reps, *fib_args):
    with mp.Pool(reps) as pool:
        pool.map(calc_fib, itertools.repeat(*fib_args, times=reps))


if __name__ == '__main__':
    REPS = 10
    ARGUMENT = [100000]
    if not os.path.exists(ARTIFACTS_DIR):
        os.makedirs(ARTIFACTS_DIR)
    with open(os.path.join(ARTIFACTS_DIR, RESULT), 'a+') as result:
        print(f'Runs with argument: {ARGUMENT}, repeated {REPS} times, mcs:', file=result)
        tasks = [
            ('Sequential', run_sequential(REPS, *ARGUMENT)),
            ('Threaded', run_with_threads(REPS, *ARGUMENT)),
            ('Processed', run_with_processes(REPS, *ARGUMENT)),
        ]
        for type, time in tasks:
            print('{:>16} {:>16}'.format(type, time.microseconds), file=result)
