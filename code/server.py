# -*- coding: utf-8 -*-
from sys import argv, version_info
import socketserver


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        raw = data.decode('utf-8')
        print(raw)
        self.request.send('JADA DET ER FINT, DET!!'.encode('utf-8'))

class KTNServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


def print_usage():
    print('Usage: python server.py <port>')

def server():
    port = int(argv[1])
    host = '127.0.0.1'

    server = KTNServer((host, port), TCPHandler)
    server.serve_forever()

# Hvis vi kjører filen med `python server.py`
if __name__ == '__main__':
    if len(argv) < 2:
        print_usage()
    elif version_info < (3, 0): 
        print('Python 3.0 or higher required')
    else:
        server()
