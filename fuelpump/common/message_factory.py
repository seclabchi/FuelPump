'''
Created on May 23, 2017

@author: zaremba
'''

import os
from fuelpump.common.message import *


class MessageFactory(object):
    '''
    classdocs
    ''' 
    seq_num = struct.unpack("I", os.urandom(4))[0]
    
    def __init__(self, params):
        '''
        Constructor
        '''
    @classmethod    
    def get_ping_req(self):
        msg = MessagePingReq()
        msg.assemble({'seq_num': MessageFactory.seq_num})
        MessageFactory.seq_num += 1
        return msg
    
    @classmethod   
    def get_ping_rsp(self, req_seq_num):
        msg = MessagePingRsp()
        msg.assemble({'seq_num': MessageFactory.seq_num, 'req_seq_num': req_seq_num})
        MessageFactory.seq_num += 1
        return msg
    
    @classmethod   
    def get_text(self, msg_txt):
        msg = MessageText()
        msg.assemble({'seq_num': MessageFactory.seq_num, 'msg_txt': msg_txt})
        MessageFactory.seq_num += 1
        return msg
        
    