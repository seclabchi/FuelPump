'''
Created on May 28, 2017

@author: zaremba
'''
import time
import socket
import binascii
import logging

from fuelpump.common.message_factory import *
from fuelpump.common.message import *
from fuelpump.common.message_datalink import *
from fuelpump.client.client_controller import *

CLIENT_VERSION = 0x01000000

class ClientConnection(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.sock = None
        self.addr = None
        self.port = 0
        self.datalink = MessageDatalink()
        
    def send_msg(self, msg):
        tx_bytes = self.datalink.encode(msg)
        tx_bytes_remain = len(tx_bytes)
        
        while tx_bytes_remain > 0:
            tx_bytes_remain -= self.sock.send(tx_bytes[:tx_bytes_remain])
        
    def connect(self, host, port):
        try:
            logging.info("Connecting to " + host + ":" + str(port) + "...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            logging.info("Connected.")
            self.send_hello()
        except Exception as e:
            logging.exception("Exception occurred attempting to connect to " + host + ":" + str(port) + " - " + repr(e))
    
    def disconnect(self):
        if None != self.sock:
            logging.info("Disconnecting...")
            self.send_goodbye_normal()
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            logging.info("Disconnected.")
            
    def send_hello(self):
        msg_hello = MessageFactory.get_hello(CLIENT_VERSION)
        self.send_msg(msg_hello)
    
    def send_goodbye_normal(self):
        msg_bye = MessageFactory.get_goodbye(Goodbye.CLIENT_SHUTDOWN_NORMAL, "Normal disconnect.")
        self.send_msg(msg_bye)
        
    def send_ping_req(self):
        msg_ping = MessageFactory.get_ping_req()
        self.send_msg(msg_ping)
        
    
if __name__ == '__main__':
    client = ClientConnection()
    result = client.connect("127.0.0.1", 2330)
    
    while True:
        client.send_ping_req()
        time.sleep(1)
    