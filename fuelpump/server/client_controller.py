'''
Created on May 28, 2017

@author: zaremba
'''

from client_connection import *

class ClientController(object):
    '''
    classdocs
    '''
    
    def __init__(self, sock, addr):
        self.client = ClientConnection(sock, addr, self)
        self.client.start()
        
    def process_msg(self, msg):
        pass
    
    def disconnect(self, reason):
        self.client.send_goodbye_normal()
        self.client.close()
        pass

