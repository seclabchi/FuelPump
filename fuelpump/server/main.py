'''
Created on May 19, 2017

@author: zaremba
'''

import signal
import sys
from secretlabcomms.common import messages_pb2

def signal_handler(signal, frame):
        print('SIGINT received.  Goodbye.')
        sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    
    msg = messages_pb2.Ping()
    base = messages_pb2.Base()
    
    msg.base.CopyFrom(base)
    msg.base.sequence_num = 23
    msg.ping_msg = "Hello, protobuf!"
    
    print str(msg)

    print('Waiting for SIGINT (Ctrl-C) to exit server...')
    signal.pause()