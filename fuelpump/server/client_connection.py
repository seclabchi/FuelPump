'''
Created on May 27, 2017

@author: zaremba
'''
import socket
import binascii
from fuelpump.common.message_datalink import MessageDatalink

class ClientConnection(object):
    '''
    classdocs
    '''

    def __init__(self, registry, sock, addr):
        '''
        Constructor
        '''
        self.registry = registry
        self.sock = sock
        self.addr = addr
        self.datalink = MessageDatalink()
        
    def close(self):
        self.sock.close()
        
    def send_msg(self, msg):
        try:
            tx_bytes = self.datalink.encode(msg)
            tx_bytes_remain = len(tx_bytes)
            
            while tx_bytes_remain > 0:
                bytes_sent = self.sock.send(tx_bytes[:tx_bytes_remain])
                tx_bytes_remain -= bytes_sent
        except Exception as e:
            print "Exception occurred with client at " + repr(self.addr) + ": " + repr(e)
            self.registry.remove(self)
    