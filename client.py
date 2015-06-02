#!/bin/python

from socket import *
import sys

class Client():
    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port

    def connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        address = (self.server_address, self.port)
        self.socket.connect(address)  
    
    def request_msg(self, n_msg):
        it = n_msg
        n_msg = str(n_msg)
        n_msg = bytes(n_msg, 'utf-8')
        self.socket.sendall(n_msg)
        print("Recebendo mensagens...")
        while it:
            it -= 1
            print(self.socket.recv(10)) 

if __name__ == '__main__':
    try:
        n_msg = int(sys.argv[1])
        if n_msg <= 0:
            raise ValueError
    except IndexError:
        print("Entre com o número de mensagens!", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("%s não é um inteiro positivo!" % n_msg, file=sys.stderr)
        sys.exit(1)

    c = Client("127.0.0.1", 45000)
    c.connect()
    c.request_msg(n_msg)

