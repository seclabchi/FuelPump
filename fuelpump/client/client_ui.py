'''
Created on May 29, 2017

@author: zaremba
'''

from Tkinter import *
from Queue import Queue
import logging
import time


class ClientUiMain():
    '''
    classdocs
    '''
    
    def __init__(self, ui_txq, ui_rxq):
        self.root = None
        self.shutdown = False
        self.txq = ui_rxq
        self.rxq = ui_txq
    
    def start_ui(self):
        logging.info('UI Hello')
        self.root = Tk()
        self.root.geometry('800x600+400+300')
        self.root.lift()
        self.root.attributes('-topmost',True)
        self.root.after_idle(self.root.attributes,'-topmost',False)
        self.root.protocol("WM_DELETE_WINDOW", self.window_closing)
        app = ClientUi(self.root)
        app.grid(column=0, row=0, sticky=(N,S,E,W))
        app.columnconfigure(0, weight=1)
        app.rowconfigure(0, weight=1) 
        
        #redefining underlying Tcl command to handle Command-Q on OSX
        #https://mail.python.org/pipermail/tkinter-discuss/2009-April/001893.html
        self.root.createcommand('exit', self.shutdown_func) 
        
        while False == self.shutdown:
            self.root.update_idletasks()
            self.root.update()
            self.process_rxq()
            
        self.txq.put('ui_done')
         
        logging.info('UI Goodbye.')
        
    def shutdown_func(self):
        logging.debug("Setting shutdown for Tkinter main loop...")
        self.shutdown = True
        
    def window_closing(self):
        logging.debug("Caught Tkinter window closing event.")
        self.txq.put('UI_QUIT')
        self.shutdown = True
        
    def process_rxq(self):
        try:
            rx_msg = self.rxq.get(False)
            logging.debug("UI got msg " + repr(rx_msg))
            self.txq.put(rx_msg, False)
        except Exception as e:
            pass
            
        
class ClientUi(Frame):
    '''
    classdocs
    '''
    
    def __init__(self, parent):
        Frame.__init__(self, parent, background="#000000")
        self.parent = parent
        self.parent.title("Secret Lab Comm - Python Client v1.0")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1) 
        self.init_ui()
        
    def init_ui(self):         
        self.connect_frame = FrameConnect(self)
        self.connect_frame.grid(row=0, column=0, sticky=(N,S,E,W), padx=0, pady=0, ipadx=0, ipady=0)
        self.text_log = Text(self, background="#999999")
        self.text_log.grid(row=1, column=0, sticky=(N, S, E, W))
        self.rowconfigure(1, weight=1000)
        self.connect_frame.update()
        connect_row_fixed_height = self.connect_frame.entry_ip.winfo_height()
        self.rowconfigure(0, minsize=connect_row_fixed_height)
        self.status_frame = FrameStatus(self)
        self.status_frame.grid(row=2, column=0, sticky=(N,S,E,W), padx=0, pady=0, ipadx=0, ipady=0)
        self.status_frame.update()
        status_row_fixed_height = self.status_frame.label_status_text.winfo_height()
        self.rowconfigure(2, minsize=status_row_fixed_height)

class FrameConnect(Frame):
    '''
    classdocs
    '''
    
    def __init__(self, parent):
        Frame.__init__(self, parent, background="#339933")   
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        self.label_ip = Label(self, text="IP address: ", background="#00FF00")
        self.label_ip.grid(row=0, column=0, sticky=(N, S, E,W)) 
        
        self.entry_ip_text = StringVar()
        self.entry_ip = Entry(self, textvariable=self.entry_ip_text, background="#FF00FF")
        self.entry_ip.grid(row=0, column=1, sticky=(N,S,E,W))
        self.entry_ip_text.set("lab.tonekids.com")
        self.columnconfigure(1, weight=1)
         
        self.label_port = Label(self, text="port: ", background="#0000FF")
        self.label_port.grid(row=0, column=2, sticky=(N,S,E,W))
         
        self.entry_port_text = StringVar()
        self.entry_port = Entry(self, textvariable=self.entry_port_text, background="#FFFF00")
        self.entry_port_text.set("2330")
        self.entry_port.grid(row=0, column=3, sticky=(N,S,E,W))
        
        self.connect_mode_button = Button(self, text="CONNECT")
        self.connect_mode_button.grid(row=0, column=4)


class FrameStatus(Frame):
    '''
    classdocs
    '''
    
    def __init__(self, parent):
        Frame.__init__(self, parent, background="#339933")   
        self.parent = parent
        self.status_text = StringVar()
        self.init_ui()
        self.toggle = False
        
    def init_ui(self):
        self.status_text.set("Hello.  Client idle.")
        self.label_status_text = Label(self, textvariable=self.status_text, background="#00FFFF")
        self.label_status_text.grid(row=0, sticky=(N,S,E,W))
        self.label_status_text.bind('<Button-1>', self.set_status_text)
        self.columnconfigure(1, weight=1)
        
    def set_status_text(self, event):
        if False == self.toggle:
            self.status_text.set("Mouse clicked.   Testing to see that the label shrinks and expands properly and can fill the screen.")
        else:
            self.status_text.set("Short label now.")
            
        self.toggle = not self.toggle
    

if __name__ == '__main__':
    txq = Queue()
    rxq = Queue()
    logging.basicConfig(filename='/tmp/slcomm_client.log', level=logging.DEBUG)
    logging_stream_handler = logging.StreamHandler()
    logging.Formatter.converter = time.gmtime
    log_formatter = logging.Formatter("%(asctime)s [%(filename)-20.20s:%(lineno)-4.4s - %(funcName)-25.25s] [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logging_stream_handler.setFormatter(log_formatter)
    logging.getLogger().addHandler(logging_stream_handler)
    ui = ClientUiMain(txq, rxq)
    ui.start_ui()