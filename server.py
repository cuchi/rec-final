#!/bin/python

from socket import *
from threading import Thread
from enum import Enum
import sys

def usage():
    print("Modo de uso:\t %s T_MSG TYPE" % sys.argv[0])
    print("Padrão:\t\t %s 10 TCP" % sys.argv[0])

class SocketType(Enum):
    TCP = 1
    UDP = 2

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
                print("oi...")
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
        while n_msg > 0:
            n_msg -= 1
            self.socket.sendto(self.msg, client_address)


if __name__ == '__main__':
    try:
        if int(sys.argv[1]) <= 0:
            raise ValueError
        s = Server("127.0.0.1", 45000, int(sys.argv[1]), SocketType[sys.argv[2]])
    except ValueError:
        print("%s não é um inteiro positivo!" % sys.argv[1], file=sys.stderr) 
        usage()
        sys.exit(1)
    except KeyError:
        usage()
        print("%s não é um tipo de socket válido! (deve ser TCP ou UDP)" % sys.argv[2])
        sys.exit(1)
    except IndexError:
        if len(sys.argv) == 2:
            s = Server("127.0.0.1", 45000, int(sys.argv[1]))
        else:
            s = Server("127.0.0.1", 45000)

    s.bind()
    s.run()
