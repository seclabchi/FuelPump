'''
Created on May 20, 2017

@author: zaremba
'''

import struct
import binascii

BYTE_STX = 0x02
BYTE_ETX = 0x03
BYTE_DLE = 0x10

class MessageDatalink(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.rx_buf = bytearray()
        self.msg_in_progress = False
        self.dle_pending = False
    
    @classmethod
    def encode(cls, msg):
        msg_bytes = msg.get_bytes()
        msg_enc = bytearray([BYTE_STX])
        msg_len = len(msg_bytes)
        msg_len_bytes = struct.pack("I", msg_len)
        msg_enc.extend(msg_len_bytes)
        msg_enc.extend(msg_bytes[0:2])
        
        for byte in msg_bytes[2:]:
            msg_enc.append(byte)
            if(BYTE_DLE == byte):
                msg_enc.append(byte)
                
        msg_enc.append(BYTE_DLE)
        msg_enc.append(BYTE_ETX)
        
        return msg_enc
        
    def decode(self, bytes, callback):
        '''
        bytes are data being read off the wire with no processing.
        
        callback gets called with a valid bytearray object once a successful decode happens.
        The bytes returned are stripped of the datalink framing and will be suitable for processing
        by the MessageBase class.
        
        This is an instance method so multiple datalink objects can be at work at the same time.
        '''
        for byte in bytes:
            if False == self.msg_in_progress:
                if BYTE_STX == byte:
                    self.msg_in_progress = True
                    self.rx_buf = bytearray()
                else:
                    print "Received character " + str(hex(byte)) + " not in msg frame."
            else:
                #msg in progress
                if BYTE_DLE == byte:
                    if True == self.dle_pending:
                        self.rx_buf.append(byte)
                        self.dle_pending = False
                    else:
                        self.dle_pending = True
                    
                elif BYTE_ETX == byte:
                    if True == self.dle_pending:
                        #end of message
                        callback(self.rx_buf)
                        self.dle_pending = False
                        self.msg_in_progress = False
                    else:
                        self.rx_buf.append(byte)
                        
                else:
                    self.rx_buf.append(byte)                    
            