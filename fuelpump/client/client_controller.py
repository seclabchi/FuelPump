'''
Created on Jun 3, 2017

@author: zaremba
'''

from fuelpump.client.client_ui import *
from fuelpump.client.client_connection import *
import logging
import threading
import time
from Queue import Queue

class ConnectState:
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2


class ClientController(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        logging.debug('client_controller CTOR')
        
        self.controller_thread = None
        
        self.connect_frame = None
        self.terminal_frame = None
        self.status_frame = None
        
        self.connect_state = ConnectState.DISCONNECTED
        
        self.ui_txq = Queue()  #Q to send msgs to UI
        self.ui_rxq = Queue()  #Q to recv msgs from UI
        
        self.ui = ClientUiMain(self.ui_txq, self.ui_rxq)

    
    def register_connect_frame(self, frame):
        self.connect_frame = frame
        
    def register_terminal_frame(self, frame):
        self.terminal_frame = frame
        
    def register_status_frame(self, frame):
        self.status_frame = frame
        
    def update_connection_state(self, state):
        logging.info('Connection state update to ' + str(state))
        
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
        logging.debug('Connection mode button pressed.')
        
    def start_controller(self):
        self.controller_thread = ControllerThread(self.ui_txq, self.ui_rxq)
        logging.debug("Starting controller thread...")
        self.controller_thread.start()
        self.ui.start_ui()  #blocks here until UI is closed.
        
    def shutdown(self):
        logging.debug("Shutting down controller thread...waiting to join...")
        self.controller_thread.shutdown()
        self.controller_thread.join()
        logging.debug("Joined controller thread.")
        
        
class ControllerThread(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self, txq, rxq):
        self.shutdown = False
        self.ui_txq = txq
        self.ui_rxq = rxq
        super(ControllerThread, self).__init__(None, self.thread_main, 'ControllerThread')
        
    def thread_main(self):
        logging.debug("Controller thread started.")
        ui_done = False
        
        while False == ui_done:
            self.ui_txq.put("Hello, UI!", False)
            
            try:
                rx_msg = self.ui_rxq.get(False)
                logging.debug("Controller got msg " + repr(rx_msg))
                if 'ui_done' == rx_msg:
                    ui_done = True
            except Exception as e:
                pass
            
            time.sleep(1)
            
        logging.debug('Controller thread done.')
    
    def shutdown(self):
        logging.info("Calling shutdown on controller...")
        self.shutdown = True
        self.join()
        logging.debug("Controller thread joined.")

if __name__ == '__main__':
    logging.basicConfig(filename='/tmp/slcomm_client.log', level=logging.DEBUG)
    logging_stream_handler = logging.StreamHandler()
    logging.Formatter.converter = time.gmtime
    log_formatter = logging.Formatter("%(asctime)s [%(filename)-20.20s:%(lineno)-4.4s - %(funcName)-25.25s] [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logging_stream_handler.setFormatter(log_formatter)
    logging.getLogger().addHandler(logging_stream_handler)
    
    controller = ClientController()
    controller.start_controller()

        