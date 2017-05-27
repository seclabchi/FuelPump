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
        raise NotImplementedError
    
    @classmethod
    def get_seq_num(cls):
        ret_seq_num = cls.seq_num
        return ret_seq_num
    
    @classmethod    
    def get_ping_req(cls):
        msg = MessagePingReq()
        msg.assemble({'seq_num': cls.get_seq_num()})
        return msg
    
    @classmethod   
    def get_ping_rsp(cls, req_seq_num):
        msg = MessagePingRsp()
        msg.assemble({'seq_num': cls.get_seq_num(), 'req_seq_num': req_seq_num})
        return msg
    
    @classmethod   
    def get_text(cls, msg_txt):
        msg = MessageText()
        msg.assemble({'seq_num': cls.get_seq_num(), 'msg_txt': msg_txt})
        return msg
    
    @classmethod
    def get_goodbye(cls, reason, reason_str):
        msg = MessageGoodbye()
        msg.assemble({'seq_num': cls.get_seq_num(), 'reason': reason, 'reason_str': reason_str})
        return msg
        
    