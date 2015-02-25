# -*- coding: utf-8 -*-
from sys import argv, version_info
import socketserver
from json import loads
from time import strftime, time

from models import *


class TCPHandler(socketserver.BaseRequestHandler):

    user = None

    def handle(self):
        while True:
            data = self.request.recv(1024)
            print('Server har fått data')
            raw = data.decode('utf-8')
            try:
                json = loads(raw)
            except ValueError:
                self.request.send('400 JSON malformed.'.encode('utf-8'))
                return
            request = Request(json['request'], json['content'])
            res = self.server.chatserver.handle_command(request)
            jsonres = to_json(res.__dict__)
            self.request.send(jsonres.encode('utf-8'))
            print('Server har sendt data.')


class KTNServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


def get_help():
    pass


class ChatServer:

    messages = []
    users = []

    def __init__(self, port, host):
        server = KTNServer((host, port), TCPHandler)
        server.chatserver = self
        server.serve_forever()

    def handle_command(self, req):
        res = Response()
        res.timestamp = strftime('%H:%M')

        res.sender = 'Martin'

        if req.request == 'msg':
            msg = Message(None, req.content)
            print(msg)
            self.messages.append(msg)
            res.response = 'info'

        elif req.request == 'names':
            res.response = 'info'
            res.content = ', '.join(map(str, users))

        elif req.request == 'help':
            res.response = 'info'
            res.content = get_help()

        else:
             res.response = 'error'
             res.content = 'Not supported command. See `help`.'
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
