# -*- coding: utf-8 -*-
import socket
from sys import argv
from json import loads

from models import *


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def run(self):
        while True:
            data = input()
            if data.strip() == '':
                continue
            i = data.find(' ')
            req = Request()
            if i == -1:
                req.request = data
            else:
                req.request = data[:i]
                req.content = data[i+1:]

            print(req)

            self.sock.send(to_json(req.__dict__).encode('utf-8'))
            res = self.sock.recv(1024)

            print(res.decode('utf-8'))



if __name__ == '__main__':
    if len(argv) < 3:
        print('Usage: python client.py <host> <port>')
    else:
        host = argv[1]
        port = int(argv[2])
        client = Client(host, port)
        client.run()

