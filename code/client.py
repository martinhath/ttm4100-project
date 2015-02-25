# -*- coding: utf-8 -*-
import socket
from sys import argv

def print_usage():
    print('Usage: python client.py <host> <port>')

def client():
    host = argv[1]
    port = int(argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    f = open('testdata.json')
    json = f.read()
    sock.send(str(json).encode('utf-8'))

if __name__ == '__main__':
    if len(argv) < 3:
        print_usage()
    else:
        client()
