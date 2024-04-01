import time
import codecs
import multiprocessing
import sys
import logging

logger = logging.getLogger()
logging.basicConfig(
    filename='artifacts/task3.log', 
    format='%(asctime)s  %(levelname)s - %(funcName)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S',
    filemode='w',
    level=logging.INFO)

def tolower(queries_queue, conn_with_rot13_encoder):
    while True:
        s = queries_queue.get()
        conn_with_rot13_encoder.send(s.lower())
        time.sleep(5)

def rot13_encoder(conn_with_tolower, conn_with_main):
    while True:
        s = conn_with_tolower.recv()
        conn_with_main.send(codecs.encode(s, 'rot_13'))

def print_result(conn_with_rot13_encoder):
    while True:
        result = conn_with_rot13_encoder.recv()
        logger.info(result)
        print(result)

if __name__ == "__main__":
    queries_queue = multiprocessing.Queue()
    conn_BA, conn_AB = multiprocessing.Pipe()
    conn_main_B, conn_B_main = multiprocessing.Pipe()

    children_processes = [
        multiprocessing.Process(target=tolower, args=(queries_queue, conn_AB,)),
        multiprocessing.Process(target=rot13_encoder, args=(conn_BA, conn_B_main,)), 
        multiprocessing.Process(target=print_result, args=(conn_main_B,))
    ]

    for process in children_processes:
        process.start()

    for line in sys.stdin:
        msg = line.rstrip('\n')
        logger.info(f'read new query: {msg}')
        queries_queue.put(msg)

    for process in children_processes:
        process.terminate()