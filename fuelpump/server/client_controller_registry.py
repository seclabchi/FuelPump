'''
Created on May 27, 2017

@author: zaremba
'''

from fuelpump.common.message import *
from fuelpump.server.client_controller import *

class ClientControllerRegistry(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.controller_list = []
        
    def add(self, sock, addr):
        controller = ClientController(sock, addr)
        self.controller_list.append(controller)
        
    def get_controllers(self):
        return self.controller_list
        
    def remove(self, controller):
        print "Removing controller for" + repr(controller.client.sock.getpeername())
        
    def shutdown_gracefully(self):
        for controller in self.controller_list:
            controller.disconnect(Goodbye.SERVER_SHUTDOWN_NORMAL)
    