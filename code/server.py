# -*- coding: utf-8 -*-
from sys import argv

import socketserver
from json import loads
from time import strftime, time

from models import *


class TCPHandler(socketserver.BaseRequestHandler):

    # Når en klient avslutter, inneholder denne listen
    # en ugyldig socket. Må fikses.
    sockets = []

    def handle(self):
        user = None
        if not self.request in self.sockets:
            self.sockets.append(self.request)

        while True:
            data = self.request.recv(1024)
            raw = data.decode('utf-8')
            try:
                json = loads(raw)
            except ValueError:
                self.request.send('400 JSON malformed.'.encode('utf-8'))
                return
            request = Request(**json)
            res, usr = self.server.chatserver.handle_command(request, user, self.request)
            user = usr

            json = to_json(res.__dict__)

            if res.broadcast:
                self.send_to_all(json)
            else:
                self.send(json, self.request)

    def send(self, res, socket):
        socket.send(res.encode('utf-8'))

    def send_to_all(self, res):
        for s in self.sockets:
            try:
                s.send(res.encode('utf-8'))
            except Exception:
                self.sockets.remove(s)


class KTNServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


def get_help():
    return "HJELP!!"


class ChatServer:

    messages = []
    users = []

    def __init__(self, port, host):
        server = KTNServer((host, port), TCPHandler)
        server.chatserver = self
        server.serve_forever()

    def send_history(self, socket):
        resp = Response()

        for msg in self.messages:
            resp.sender = msg.user.username
            resp.timestamp = msg.timestamp
            resp.content = msg.message

            json = to_json(resp.__dict__)
            socket.send(json.encode('utf-8'))

    def handle_command(self, req, user=None, socket=None):
        res = Response()
        res.timestamp = strftime('%H:%M')


        if req.request == 'login':
            if user:
                req.request = 'help'
                return handle_command(self, req, user)
            user = User(req.content, '')
            self.users.append(user)
            res.sender = 'Server'
            res.response = 'message'
            res.content = '{} logged in'.format(user.username)
            res.broadcast = True

            self.send_history(socket)

        elif req.request == 'help':
            res.response = 'info'
            res.content = get_help()
            res.sender = 'Server'
            return res, user

        elif not user:
            """
            litt hacky å ha denne, men tanken er at vi ikke trenger å
            sjekke om man er logget inn før etter vi har sjekket
            om kommandoen er login eller help, siden de ikke 
            krever at man er logget inn.
            """
            res.response = 'error'
            res.content = 'Not supported command. See `help`.'
            return res, None

        elif req.request == 'msg':
            msg = Message(user, req.content, res.timestamp)
            self.messages.append(msg)
            res.response = 'message'
            res.content = msg.message
            res.sender = user.username
            res.broadcast = True

        elif req.request == 'names':
            res.response = 'info'
            res.content = ', '.join(map(str, self.users))
            res.sender = 'Server'

        elif req.request == 'logout':
            res.response = 'message'
            res.sender = 'Server'
            res.content = '{} loged out.'.format(user.username)
            res.broadcast = True
            user = None
            return res, None

        else:
            res.response = 'error'
            res.sender = 'Server'
            res.content = 'Not supported command. See `help`.'

        return res, user



# Hvis vi kjører filen med `python server.py`
if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: python server.py <port>')
    else:
        port = int(argv[1])
        host = '127.0.0.1'
        ChatServer(port, host)
