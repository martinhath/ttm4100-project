# -*- coding: utf-8 -*-
from sys import argv

import socketserver
from json import loads
from time import strftime, time

from models import *



class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    users = []
    messages = []
    sockets = []

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


class RequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.socket = self.request
        self.user = None

        while True:
            data = self.request.recv(1024).decode('utf-8')
            try:
                json = loads(data)
            except ValueError:
                return
            request = Request(**json)
            request.sender = self.user
            '''
            Vi har nå et Request-objekt.
            Vi vil bruke ChatServer sin funksjon,
            `handle` til å håndtere denne.`
            '''

            if request.request == 'help':
                self.send_help()
                continue

            if self.user:
                self.handle_logged_in(request)
            else:
                self.handle_not_logged_in(request)

    def handle_logged_in(self, request):
        type = request.request
        if type == 'msg':
            self.msg(request)
        elif type == 'logout':
            self.logout()
        elif type == 'names':
            self.names()
        # handle errors
        elif type == 'login':
            res = self.create_response(
                    'Server',
                    'error',
                    'You need to log out in order to log in.')
            self.send_response(res)

    def handle_not_logged_in(self, request):
        type = request.request
        if type == 'login':
            self.login(request)
            self.server.sockets.append(self.socket)
            self.send_log()
        else:
            self.send_login_error()

    def login(self, request):
        '''Håndterer inloggingslogikk'''
        # svarer klienten
        self.user = User(request.content)
        res = self.create_response(
                'login',
                'info',
                self.user.username)
        self.send_response(res)
        # forteller alle om login
        res = self.create_response(
                'Server',
                'message',
                'User {} logged in.'.format(self.user.username))
        self.broadcast_response(res)

        self.server.users.append(self.user)

    def logout(self):
        '''Håndterer utloggingslogikk'''
        # svarer klienten
        res = self.create_response(
                'logout',
                'info',
                self.user.username)
        self.send_response(res)
        # forteller alle om logout
        res = self.create_response(
                'Server',
                'message',
                'User {} logged out.'.format(self.user.username))
        self.server.users.remove(self.user)
        self.user = None
        self.broadcast_response(res)
        self.server.sockets.remove(self.socket)

    def names(self):
        '''Håndterer logikk rundt `names`'''
        usernames = [u.username for u in self.server.users]
        res = self.create_response(
                'Server',
                'info',
                ", ".join(usernames))
        self.send_response(res)
            
    def msg(self, request):
        '''Håndterer logikk rundt å sende meldinger'''
        res = self.create_response(self.user.username,
                              'message',
                              request.content)
        self.broadcast_response(res)

    def create_response(self, sender, response, content, time=None):
        '''Lager et Response-objekt basert på parameterene'''
        res = Response()
        if time == None:
            res.timestamp = strftime('%H:%M')
        else: res.timestamp = time
        res.sender = sender
        res.response = response
        res.content = content
        return res

    def send_response(self, res):
        '''Sender responsen'''
        d = res.__dict__
        if res.response == 'history':
            d['content'] = [c.__dict__ for c in d['content']]
        json = to_json(res.__dict__)
        self.socket.send(json.encode('utf-8'))

        self.log(res)

    def broadcast_response(self, res):
        '''Sender responsen til alle som er logget inn'''
        json = to_json(res.__dict__)
        for s in self.server.sockets:
            try:
                s.send(json.encode('utf-8'))
            except Exception as e:
                self.log(e)
                self.server.sockets.remove(s)
        self.log(res)
        self.server.messages.append(Message(res.sender,
            res.content, res.timestamp))

    def send_log(self):
        msgs = [self.create_response(m.user, 'message', m.message, m.timestamp)\
                for m in self.server.messages]
        res = self.create_response('Server',
                                'history',
                                msgs)
        self.send_response(res)

    def send_help(self):
        '''Lager og sender hjelpetekst'''
        res = self.create_response('Server',
                            'info',
                            'Available commands are:\n' + 
                            '\thelp\n' + 
                            '\tlogin <username>\n' + 
                            'If you are logged in:\n' + 
                            '\tmsg <message>\n' + 
                            '\tnames\n' + 
                            '\tlogout')
        self.send_response(res)

    def send_login_error(self):
        '''Sender feil når bruker ikke er logget inn, men 
           prøverå gjøre noe som krever innloggelse'''
        res = self.create_response('Server',
                            'error',
                            'You must be logged in to do this.')
        self.send_response(res)

    def log(self, s):
        s = str(s).replace('\n', "\n")
        print('[LOG]: ' + s[:80])




if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: python server.py <port>')
    else:
        port = int(argv[1])
        host = '127.0.0.1'
        server = ChatServer((host, port), RequestHandler)
        server.serve_forever()
