# -*- coding: utf-8 -*-
import socket
from sys import argv, stdout, exit
from json import loads
from time import sleep
from time import strftime

from threading import Thread

from pprint import pprint

from models import *

class Client:

    stop = False
    
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    '''
    Her tar vi i mot ting fra serveren.
    '''
    def handle_network(self):
        sender = ''
        while not self.stop:
            self.print_pre(sender)
            res = self.sock.recv(10024)
            if res == b'':
                self.stop = True
                break

            res_dict = loads(res.decode('utf-8'))
            res = Response(**res_dict)

            if res.response == 'message':
                if res.sender != sender:
                    self.print_response(res)

            elif res.response == 'info':
                if res.sender == 'login':
                    sender = res.content
                elif res.sender == 'logout':
                    sender = ''
                else:
                    self.print_response(res)

            elif res.response == 'error':
                self.print_response(res)

            elif res.response == 'history':
                self.print_history(res)


    '''
    Her leser vi input fra brukeren, parser det,
    og sender en request til serveren.
    '''
    def handle_gui(self):
        while not self.stop:
            data = input()
            if data.strip() == '':
                continue
            req = Request()

            cmd = self.get_command(data)
            if not cmd:
                req.request = 'msg'
                req.content = data
            else:
                req.request = cmd
                req.content = data[len(cmd)+2:]

            self.sock.send(to_json(req.__dict__).encode('utf-8'))
            sleep(0.1)

    def get_command(self, string):
        if string.startswith('/'):
            return string.split()[0][1:]
        return None

    def run(self):
        self.network_thread = Thread(target=self.handle_network)
        self.gui_thread = Thread(target=self.handle_gui)
        self.network_thread.start()
        self.gui_thread.start()

    def print_pre(self, username):
        if not username:
            username = 'default'
        stdout.write('\r[{:5}] {:14}| '.format(
                strftime('%H:%M'), username))

    def print_history(self, res):
        msgs = res.content
        for m in msgs:
            r = Response(**m)
            self.print_response(r)


    def print_response(self, res):
        print('\r[{:5}] {:14}| {}'.format(
                res.timestamp, res.sender, res.content))



if __name__ == '__main__':
    if len(argv) < 3:
        print('Usage: python client.py <host> <port>')
    else:
        host = argv[1]
        port = int(argv[2])
        client = Client(host, port)
        client.run()

