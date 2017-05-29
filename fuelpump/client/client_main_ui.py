'''
Created on May 29, 2017

@author: zaremba
'''

from Tkinter import *
from ttk import *

class ClientMainUi(Frame):
    '''
    classdocs
    '''
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        self.parent.title("Secret Lab Comm - Python Client v1.0")
        self.pack(fill=BOTH, expand=1)
        
        Style().configure("TFrame", background="#333")
        

def main():
    root = Tk()
    root.geometry('640x480+600+400')
    app = ClientMainUi(root)
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    root.mainloop()

if __name__ == '__main__':
    main()