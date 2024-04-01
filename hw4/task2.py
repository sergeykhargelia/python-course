import math
import os
import timeit
import concurrent.futures
import logging

logger = logging.getLogger()
logging.basicConfig(
    filename='artifacts/task2/timestamps.log', 
    format='%(asctime)s  %(levelname)s - %(funcName)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S',
    filemode='w',
    level=logging.INFO)

def integrate_batch(args):
    f, a, b, n_jobs, n_iter, batch_id = args
    logger.info(f'started to integrate batch {batch_id}')
    
    result = 0
    step = (b - a) / n_iter
    batch_size = n_iter // n_jobs
    start = batch_size * batch_id
    end = min(n_iter, batch_size * (batch_id + 1))

    for i in range(start, end):
        result += f(a + i * step)

    logger.info(f'finished to integate batch {batch_id}')

    return result * step

def integrate(f, a, b, create_executor, *, n_jobs=1, n_iter=10000000):
    logger.info(f'started to integrate with n_jobs = {n_jobs} and n_iter = {n_iter}')
    executor = create_executor(n_jobs)
    args = [(f, a, b, n_jobs, n_iter, job_id) for job_id in range(n_jobs)]
    result = sum(executor.map(integrate_batch, args))
    logger.info(f'finished to integrate with n_jobs = {n_jobs} and n_iter = {n_iter}')

def measure_integration_time(create_executor, executor_name):
    logger.info(f'started time measuring for {executor_name}')
    output_filename = f'./artifacts/task2/{executor_name}.txt'
    with open(output_filename, 'w') as out:
        out.write(f'time measuring for {executor_name}\n')
        for n_jobs in range(1, 2 * os.cpu_count() + 1):
            start = timeit.default_timer()
            integrate(math.cos, 0, math.pi / 2, create_executor, n_jobs=n_jobs)
            end = timeit.default_timer()
            out.write(f'n_jobs = {n_jobs}: {end - start}\n')

    logger.info(f'finished time measuring for {executor_name}')

if __name__ == '__main__':
    measure_integration_time(lambda n_jobs: concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs), 'thread_pool_executor')
    measure_integration_time(lambda n_jobs: concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs), 'process_pool_executor')