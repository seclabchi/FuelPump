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
    
    
    def __init__(self, message_type):
        '''
        Constructor
        '''
    
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
        
        
    @classmethod
    def decode(cls, msg):
        pass