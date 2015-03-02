# -*- coding: utf-8 -*-
import socket
from sys import argv, stdout
from json import loads
from time import sleep
from time import strftime

from threading import Thread

from pprint import pprint

from models import *

class Client:
    
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    '''
    Her tar vi i mot ting fra serveren.
    '''
    def handle_network(self):
        sender = ''
        while True:
            self.print_pre(sender)
            res = self.sock.recv(1024)

            res_dict = loads(res.decode('utf-8'))
            res = Response(**res_dict)

            if res.response == 'message':
                if res.sender != sender:
                    self.print_response(res)

            elif res.response == 'info':
                if res.content == 'logged in':
                    sender = res.sender
                self.print_response(res)

            elif res.response == 'error':
                self.print_response(res)

            elif res.response == 'history':
                self.print_response(res)


    '''
    Her leser vi input fra brukeren, parser det,
    og sender en request til serveren.
    '''
    def handle_gui(self):
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

            self.sock.send(to_json(req.__dict__).encode('utf-8'))
            sleep(0.1)


    def run(self):
        network_thread = Thread(target=self.handle_network)
        gui_thread = Thread(target=self.handle_gui)
        network_thread.start()
        gui_thread.start()

    def print_pre(self, username, time=strftime('%H:%M')):
        if not username:
            username = 'default'
        stdout.write('\r[{:5}] {:14}| '.format(
                time, username))

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

