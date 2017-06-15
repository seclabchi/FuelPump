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
        self.ui_done = True
        super(ControllerThread, self).__init__(None, self.thread_main, 'ControllerThread')
        
    def thread_main(self):
        rx_mon = UiQMonitor(self.ui_rxq, self.ui_msg_received)
        rx_mon.start()
        
        logging.debug("Controller thread started.")
        
        while False == self.ui_done:
            self.ui_txq.put("Hello, UI!", False)
            #add event waiter for tx here
            
        logging.debug('Controller thread done.')
    
    def shutdown(self):
        logging.info("Calling shutdown on controller...")
        self.shutdown = True
        self.join()
        logging.debug("Controller thread joined.")
        
        
class UiQMonitor(threading.Thread):
    '''
    classdocs
    '''
    
    def __init__(self, rxq, rx_msg_callback):
        self.rxq = rxq
        self.callback = rx_msg_callback
        super(UiQMonitor, self).__init__(None, self.run_func, "UiQMonitorThread")
        
    def shutdown(self):
        logging.debug("Shutdown received.")
        self.rxq.put(False, "SELF_QUIT")
        self.join()
        logging.debug("Self joined.")
        
    def run_func(self):
        logging.debug('Top of thread loop.')
        while True:
            rx_msg = self.rxq.get(True)
            logging.debug("Got msg " + repr(rx_msg))
            if ('UI_QUIT' == rx_msg) or ('SELF_QUIT' == rx_msg):
                break
            
        #figure out stop logic
        logging.debug('Exiting thread loop.')
    

if __name__ == '__main__':
    logging.basicConfig(filename='/tmp/slcomm_client.log', level=logging.DEBUG)
    logging_stream_handler = logging.StreamHandler()
    logging.Formatter.converter = time.gmtime
    log_formatter = logging.Formatter("%(asctime)s [%(filename)-20.20s:%(lineno)-4.4s - %(funcName)-25.25s] [%(threadName)-18.18s] [%(levelname)-5.5s]  %(message)s")
    logging_stream_handler.setFormatter(log_formatter)
    logging.getLogger().addHandler(logging_stream_handler)
    
    controller = ClientController()
    controller.start_controller()

        