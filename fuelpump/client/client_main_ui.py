'''
Created on May 29, 2017

@author: zaremba
'''

from Tkinter import *
from test.test_mutants import Parent
from fuelpump.client.client_controller import *

class ClientMainUi(Frame):
    '''
    classdocs
    '''
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="#000000")
        self.parent = parent
        self.controller = controller
        self.parent.title("Secret Lab Comm - Python Client v1.0")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1) 
        self.init_ui()
        
    def init_ui(self):         
        self.connect_frame = FrameConnect(self, self.controller)
        self.connect_frame.grid(row=0, column=0, sticky=(N,S,E,W), padx=0, pady=0, ipadx=0, ipady=0)
        self.text_log = Text(self, background="#999999")
        self.text_log.grid(row=1, column=0, sticky=(N, S, E, W))
        self.rowconfigure(1, weight=1000)
        self.connect_frame.update()
        connect_row_fixed_height = self.connect_frame.entry_ip.winfo_height()
        self.rowconfigure(0, minsize=connect_row_fixed_height)

class FrameConnect(Frame):
    '''
    classdocs
    '''
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="#339933")   
        self.parent = parent
        self.controller = controller
        controller.register_connect_frame(self)
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
        
        self.connect_mode_button = Button(self, text="CONNECT", command=self.controller.connect_pressed)
        self.connect_mode_button.grid(row=0, column=4)



def main():
    controller = ClientController()
    root = Tk()
    root.geometry('800x600+400+300')
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    app = ClientMainUi(root, controller)
    app.grid(column=0, row=0, sticky=(N,S,E,W))
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1) 
    root.mainloop()

if __name__ == '__main__':
    main()