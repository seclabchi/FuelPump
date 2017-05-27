'''
Created on May 19, 2017

@author: zaremba
'''

import signal
import sys
import socket

from fuelpump.server.client_connection_registry import *
from fuelpump.server.client_connection import *
from fuelpump.common.message_factory import MessageFactory
from fuelpump.common.messages_pb2 import *
from fuelpump.common.message import MessageGoodbye

IP_ADDR = "0.0.0.0"
IP_PORT = 2330
MAX_CONNECTION_QUEUE = 10

client_registry = ClientConnectionRegistry()

def signal_handler(signal, frame):
        print('SIGINT received.  Goodbye.')
        for client in client_registry.get_clients():
            msg_goodbye = MessageFactory.get_goodbye(Goodbye.SERVER_SHUTDOWN, "Server is exiting on signal.")
            client.send_msg(msg_goodbye)
            client.close()
        sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    
    listener_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener_sock.bind((IP_ADDR, IP_PORT))
    listener_sock.listen(MAX_CONNECTION_QUEUE)
    
    while(True):
        (client_sock, client_addr) = listener_sock.accept()
        print "New connection from " + repr(client_addr)
        client_registry.add(ClientConnection(client_registry, client_sock, client_addr))
        