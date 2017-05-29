'''
Created on May 27, 2017

@author: zaremba
'''
import socket
import time
import binascii
import threading
import select
from fuelpump.common.message_datalink import MessageDatalink
from fuelpump.common.message_factory import *
from fuelpump.common.message import *

class ClientConnection(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, sock, addr, controller):
        '''
        Constructor
        '''
        self.sock = sock
        self.addr = addr
        self.controller = controller
        self.datalink = MessageDatalink()
        self.shutdown = False
        self.datalink = MessageDatalink()
        self.sock.setblocking(0)
        super(ClientConnection, self).__init__(None, self.thread_main)
        
    def close(self):
        self.shutdown = True
        self.join()
        self.sock.close()
        
    def send_msg(self, msg):
        try:
            tx_bytes = self.datalink.encode(msg)
            tx_bytes_remain = len(tx_bytes)
            
            while tx_bytes_remain > 0:
                bytes_sent = self.sock.send(tx_bytes[:tx_bytes_remain])
                tx_bytes_remain -= bytes_sent
        except Exception as e:
            print "Exception occurred with client at " + repr(self.sock.getpeername()) + ": " + repr(e)
            self.registry.remove(self)
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            
    def thread_main(self):
        
        sock_fd = self.sock.fileno()
        kqueue_obj = select.kqueue()
        kevent_obj = select.kevent(sock_fd)
        kevent_obj.filter = select.KQ_FILTER_READ
        kevent_obj.flags = select.KQ_EV_ADD | select.KQ_EV_ENABLE
        
        kqueue_obj.control([kevent_obj], 0, 0)
        
        while False == self.shutdown:
            print "Top of thread loop"
            
            kqueue_results = kqueue_obj.control([], 1, None)
            
            for event in kqueue_results:
                if event.filter == select.KQ_FILTER_READ:
                    print "Got kqueue FILTER_READ"
                    bytes_rx = self.sock.recv(1024)
                    num_bytes_rx = len(bytes_rx)
                    print "Received " + str(num_bytes_rx) + " bytes from client " + repr(self.sock.getpeername())
                    bytes_rx = bytearray(bytes_rx)
                    self.datalink.decode(bytes_rx, self.received_msg_handler)
                else:
                    print "Unknown kqueue filter hit: " + repr(event)
                    
        print "Exiting thread."
        
    def received_msg_handler(self, msg_bytes):
        msg_len = struct.unpack("I", msg_bytes[0:4])[0]
        msg_type = struct.unpack("H", msg_bytes[4:6])[0]
        
        rx_msg = MessageType.msg_from_type(msg_type)
        
        if None == rx_msg:
            raise Exception("Unknown message type " + str(msg_type))
        
        rx_msg.create_from_bytes(msg_bytes[4:])
        print "Received " + MessageType.str_from_type(msg_type) + " from client " + repr(self.sock.getpeername()) + ":   " + str(rx_msg.proto) 
        self.controller.process_msg(rx_msg)
    
    def send_hello_msg(self):
        msg_hello = MessageFactory.get_hello(self.server_version)
        self.send_msg(msg_hello)
        
    def send_goodbye_normal(self):
        msg_bye = MessageFactory.get_goodbye(Goodbye.SERVER_SHUTDOWN_NORMAL, "Server shutting down.  Goodbye.")
        self.send_msg(msg_bye)