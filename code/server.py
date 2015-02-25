# -*- coding: utf-8 -*-
from sys import argv, version_info
import socketserver
from json import loads

from models import *


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        raw = data.decode('utf-8')
        try:
            json = loads(raw)
            request = json['request']
            content = json['content']
            self.server.chatserver.handle_command(request, content)
        except ValueError:
            self.request.send('400 JSON malformed.'.encode('utf-8'))


class KTNServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)



class ChatServer:

    def __init__(self, port, host):
        server = KTNServer((host, port), TCPHandler)
        server.chatserver = self
        server.serve_forever()

        self.messages = []
        self.users = []

    def handle_command(self, req, content):
        print('req:', req)
        print('content:', content)
        if req == 'msg':
            msg = Message(None, content)
            mesasges.append(msg)
            #broadcast
        else:
             pass



# Hvis vi kjører filen med `python server.py`
if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: python server.py <port>')
    elif version_info < (3, 0): 
        print('Python 3.0 or higher required')
    else:
        port = int(argv[1])
        host = '127.0.0.1'
        ChatServer(port, host)
