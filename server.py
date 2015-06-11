#!/bin/python

from socket import *
from threading import Thread
from enum import Enum
from getopt import *
import sys

class SocketType(Enum):
    TCP = tcp = 1
    UDP = udp = 2

class Server():
    def __init__(self, address, port, msg_size=10, s_type=SocketType.TCP):
        self.address = address
        self.port = port
        self.thread_cnt = 1
        self.msg_size = msg_size
        self.s_type = s_type

    def bind(self):
        if self.s_type == SocketType.TCP:
            self.socket = socket(AF_INET, SOCK_STREAM)
            address = (self.address, self.port)
            self.socket.bind(address)
            self.socket.listen(1)
            print("Escutando em: %s:%s" % address)
            print("Tamanho da mensagem: %s" % self.msg_size)
        else:
            self.socket = socket(AF_INET, SOCK_DGRAM)
            address = (self.address, self.port)
            self.socket.bind(address)
            print("Esperando em: %s:%s" % address)
            print("Tamanho da mensagem: %s" % self.msg_size)

    def run(self):
        self.msg = b'0' * self.msg_size
        if self.s_type == SocketType.TCP:
            while True:
                connection, client_address = self.socket.accept()
                t_args = (connection, client_address, self.thread_cnt)
                t = Thread(target=self.send_msgs_tcp, args=t_args)
                t.start()
                self.thread_cnt += 1
        else:
            while True:
                n_msg, client_address = self.socket.recvfrom(1024) 
                n_msg = int(n_msg)
                t_args = (n_msg, client_address, self.thread_cnt)
                t = Thread(target=self.send_msgs_udp, args=t_args)
                t.start()
                self.thread_cnt += 1
    
    def send_msgs_tcp(self, connection, client_address, thread_n):
        n_msg = int(connection.recv(8))
        info = (thread_n, n_msg, client_address[0])
        print("## THREAD %s: enviando %s mensagens para %s" % info)
        while n_msg > 0:
            n_msg -= 1
            try:
                connection.sendall(self.msg)
            except ConnectionResetError:
                print("## THREAD %s: concluída com erro." % thread_n)
                return
        print("## THREAD %s: concluído!" % thread_n)

    def send_msgs_udp(self, n_msg, client_address, thread_n):
        info = (thread_n, n_msg, client_address[0])
        print("## THREAD %s: enviando %s mensagens para %s" % info)
        while n_msg > 0:
            n_msg -= 1
            self.socket.sendto(self.msg, client_address)
        print("## THREAD %s: concluído!" % thread_n)

def usage():
    print("Modo de uso:\t %s -s tam_msg -t tipo_socket" % sys.argv[0])

if __name__ == '__main__':
    server_args = dict()

    try:
        opts, args = getopt(sys.argv[1:], "s:t:")
        if args:
            raise GetoptError("Argumentos inválidos")
    except GetoptError as e:
        print(e)
        usage()
        sys.exit(1)
    for o, a in opts:
        if o == "-s":
            try:
                a = int(a)
                server_args["msg_size"] = a
                if a <= 0:
                    raise ValueError
            except ValueError:
                print("%s deve ser um inteiro positivo." % a, file=sys.stderr) 
                usage()
                sys.exit(1)
        if o == "-t":
            try:
                server_args["s_type"] = SocketType[a]
            except KeyError:
                print("%s não é um tipo de socket válido" % a, file=sys.stderr)
                usage()
                sys.exit(2)
    
    s = Server("127.0.0.1", 45000, **server_args) 
    s.bind()
    s.run()
