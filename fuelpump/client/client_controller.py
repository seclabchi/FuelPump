'''
Created on Jun 3, 2017

@author: zaremba
'''

from fuelpump.client.client_main_ui import *

class ConnectState:
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2


class ClientController(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.connect_frame = None
        self.terminal_frame = None
        self.connect_state = ConnectState.DISCONNECTED
    
    def register_connect_frame(self, frame):
        self.connect_frame = frame
        
    def register_terminal_frame(self, frame):
        self.terminal_frame = frame
        
    def update_connection_state(self, state):
        if ConnectState.DISCONNECTED == state:
            self.connect_frame.connect_mode_button.configure(text="CONNECT")
        elif ConnectState.CONNECTING == state:
            self.connect_frame.connect_mode_button.configure(text="CONNECTING")
        elif ConnectState.CONNECTED == state:
            self.connect_frame.connect_mode_button.configure(text="DISCONNECT")
        else:
            raise Exception("Unknown connection state")
        
        self.connect_state = state
        
    def connect_pressed(self):
        print "Connect pressed"
        

    
        