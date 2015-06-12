#!/bin/python

from socket import *
from enum import Enum
from threading import Thread
from getopt import *
import sys
import time

class SocketType(Enum):
    TCP = tcp = 1
    UDP = udp = 2

class Client():
    def __init__(self, server_address, server_port, msg_size=10, s_type=SocketType.TCP):
        self.server_address = server_address
        self.server_port = server_port
        self.msg_size = msg_size
        self.s_type = s_type

    def connect(self):
        if self.s_type == SocketType.TCP:
            self.socket = socket(AF_INET, SOCK_STREAM)
            address = (self.server_address, self.port)
            self.socket.connect(address)  
        else:
            self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.settimeout(1)

    def request_msg(self, n_msg):
        self.it = n_msg
        n_msg = str(n_msg)
        n_msg = bytes(n_msg, 'utf-8')
        start = time.time()
        try:
            if self.s_type == SocketType.TCP:
                self.socket.sendall(n_msg)
                while self.it:
                    self.it -= 1
                    msg = self.socket.recv(self.msg_size) 
            else:
                addr = (self.server_address, self.server_port)
                self.socket.sendto(n_msg, addr)
                while self.it:
                    self.it -= 1
                    msg = self.socket.recvfrom(self.msg_size) 
        except timeout:
            print("Erro de Timeout!", file=sys.stderr)
            print(self.it)
            print("%s mensagens não recebidas" % self.it, file=sys.stderr)
            sys.exit(5)
        end = time.time()
        elapsed_time = end - start
        n_msg = str(n_msg, "utf-8")
        print("%s" % elapsed_time)

def usage():
    print("Modo de uso:\n %s -s tam_msg -t tipo_socket -n num_msgs\n\n" % sys.argv[0])    
    
if __name__ == '__main__':
    client_args = dict()

    n_msg = 10
    try:
        opts, args = getopt(sys.argv[1:], "s:t:n:")
        if args or len(opts) == 0:
            raise GetoptError("Argumentos inválidos")
    except GetoptError as e:
        print(e)
        usage()
        sys.exit(1)
    for o, a in opts:
        if o == "-s":
            try:
                a = int(a)
                client_args["msg_size"] = a
                if a <= 0:
                    raise ValueError
            except ValueError:
                print("%s deve ser um inteiro positivo." % a, file=sys.stderr) 
                usage()
                sys.exit(1)
        if o == "-t":
            try:
                client_args["s_type"] = SocketType[a]
            except KeyError:
                print("%s não é um tipo de socket válido" % a, file=sys.stderr)
                usage()
                sys.exit(2)
        if o == "-n":
            try:
                a = int(a)
                n_msg = a
                if a <= 0:
                    raise ValueError
            except ValueError:
                print("%s deve ser um inteiro positivo." % a, file=sys.stderr) 
                usage()
                sys.exit(3)

    c = Client("127.0.0.1", 45000, **client_args)
    c.connect()
    c.request_msg(n_msg)
    sys.exit(0)

