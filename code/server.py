# -*- coding: utf-8 -*-
from sys import argv, version_info
import socketserver
from json import loads
from time import strftime, time

from models import *


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        raw = data.decode('utf-8')
        try:
            json = loads(raw)
            request = Request(json['request'], json['content'])
            res = self.server.chatserver.handle_command(request)
            self.request.send(res.encode('utf-8'))
        except ValueError:
            self.request.send('400 JSON malformed.'.encode('utf-8'))


class KTNServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)



class ChatServer:

    messages = []
    users = []

    def __init__(self, port, host):
        server = KTNServer((host, port), TCPHandler)
        server.chatserver = self
        server.serve_forever()

    def handle_command(self, req):
        res = Response()
        res.timestamp = strftime('%H:%M', time())

        res.sender = 'Martin'

        if req.request == 'msg':
            msg = Message(None, req.content)
            self.messages.append(msg)
            res.response = 'info'
            #broadcast
        else:
             pass
        return res



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
