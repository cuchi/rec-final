#!/bin/python

from socket import *
from threading import Thread
import sys

class Server():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.thread_cnt = 1

    def bind(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        address = (self.address, self.port)
        self.socket.bind(address)
        self.socket.listen(1)
        print("Escutando em: %s:%s" % address)

    def run(self):
        while True:
            connection, client_address = self.socket.accept()
            t_args = (connection, client_address, self.thread_cnt)
            t = Thread(target=self.send_msgs, args=t_args)
            t.start()
            self.thread_cnt += 1
    
    def send_msgs(self, connection, client_address, thread_n):
        n_msg = int(connection.recv(8))
        info = (thread_n, n_msg, client_address[0])
        print("## THREAD %s: enviando %s mensagens para %s" % info)
        while n_msg > 0:
            n_msg -= 1
            connection.sendall(b'0123456789')
        print("## THREAD %s: concluído!" % thread_n)

if __name__ == '__main__':
    s = Server("127.0.0.1", 45000)
    s.bind()
    s.run()
