import threading
import multiprocessing
from contextlib import contextmanager
from timeit import default_timer
from typing import Final

@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start

def fib(n):
    if n <= 1:
        return n
    
    return fib(n - 1) + fib(n - 2)


N_TIMES: Final = 10

def calc_fib_concurrently(create_worker, calculator_name, n_times=N_TIMES):
    with elapsed_timer() as timer:
        tasks = []
        for i in range(n_times):
            task = create_worker()
            task.start()
            tasks.append(task)

        for task in tasks:
            task.join()

        print(f'time for {calculator_name}: {timer()}')

def calc_fib_synchronously(n_fib, n_times=N_TIMES):
    with elapsed_timer() as timer:
        for _ in range(n_times):
            fib(n)

        print(f'time for synchronous: {timer()}')

if __name__ == '__main__':
    n = 35
    calc_fib_concurrently(lambda: threading.Thread(target=fib, args=(n,)), 'threading')
    calc_fib_concurrently(lambda: multiprocessing.Process(target=fib, args=(n,)), 'multiprocessing')
    calc_fib_synchronously(n)