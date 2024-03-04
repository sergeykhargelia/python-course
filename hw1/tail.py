import sys
from typing import Final
import os

def tail(f, number_of_lines):
    result = []
    
    BLOCK_SIZE: Final = 4096
    blocks_count = 1

    while len(result) <= number_of_lines:
        try:
            # read blocks_count * BLOCK_SIZE bytes from the end of file
            f.seek(-blocks_count * BLOCK_SIZE, os.SEEK_END)
        except IOError:
            f.seek(0)
            result = f.readlines()
            break
        
        result = f.readlines()
        blocks_count += 1

    return result[-number_of_lines:]

NUMBER_OF_LINES_FOR_STDIN: Final = 17
NUMBER_OF_LINES_FOR_FILE: Final = 10

if len(sys.argv) == 1 or sys.argv[1] == '-':
    # there is no files, read from stdin
    print(''.join(sys.stdin.readlines()[-NUMBER_OF_LINES_FOR_STDIN:]), end='')
else:
    was_success = False

    # print headers iff number of files > 1
    need_header = len(sys.argv) > 2

    for file_name in sys.argv[1:]:
        try:
            with open(file_name, 'r') as file:
                if need_header:
                    if was_success:
                        print()
                    print(f'==> {file_name} <==')

                print(''.join(tail(file, NUMBER_OF_LINES_FOR_FILE)), end='')
                was_success = True
        except FileNotFoundError:
            print(file_name + ': no such file')
