# -*- coding: utf-8 -*-
from sys import argv, version_info


def print_usage():
    print('Usage: python server.py <port>')

def server():
    port = argv[1]
    print('Port: ', port)

# Hvis vi kjører filen med `python server.py`
if __name__ == '__main__':
    if len(argv) < 2:
        print_usage()
    elif version_info < (3, 0): 
        print('Python 3.0 or higher required')
    else:
        server()
