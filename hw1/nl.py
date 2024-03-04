import sys
from typing import Final

# default parameters of nl command
NUMBER_WIDTH: Final = 6
SEPARATOR: Final = '\t'

def add_line_number(line, number):
    return f'{number:>{NUMBER_WIDTH}}{SEPARATOR}{line}'
    
if len(sys.argv) == 1 or sys.argv[1] == '-':
    # there is no files, read from stdin
    for number, line in enumerate(sys.stdin, start=1):
        print(add_line_number(line.rstrip('\n'), number))
else:
    # common line number for all files
    line_number = 1

    for file_name in sys.argv[1:]:
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    print(add_line_number(line.rstrip('\n'), line_number))
                    line_number += 1
        except FileNotFoundError:
            print(file_name + ': no such file')
