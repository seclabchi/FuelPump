'''
Created on May 20, 2017

@author: zaremba
'''

from fuelpump.common.messages_pb2 import *
import struct

class MessageType:
    NONE = 0
    PING_REQ = 1
    PING_RSP = 2
    TEXT = 3
    GOODBYE = 4
    HELLO = 5
    
    @staticmethod
    def str_from_type(msg_type):
        str_val = {
            MessageType.NONE: "NONE",
            MessageType.PING_REQ: "PING_REQ",
            MessageType.PING_RSP: "PING_RSP",
            MessageType.TEXT: "TEXT",
            MessageType.GOODBYE: "GOODBYE",
            MessageType.HELLO: "HELLO",
        }.get(msg_type, "NONE")
        
        return str_val
    
    @staticmethod
    def msg_from_type(msg_type):
        new_msg = {
            MessageType.NONE: None,
            MessageType.PING_REQ: MessagePingReq(),
            MessageType.PING_RSP: MessagePingRsp(),
            MessageType.TEXT: MessageText(),
            MessageType.GOODBYE: MessageGoodbye(),
            MessageType.HELLO: MessageHello(),
        }.get(msg_type, None)
        
        return new_msg
    
class MessageBase(object):
    '''
    classdocs
    '''
        
    def __new__(cls, *args, **kwargs):
        if cls is MessageBase:
            raise TypeError("base class may not be instantiated")
        return object.__new__(cls, *args, **kwargs)
    
    def __init__(self):
        self.proto = None
        self.is_completely_assembled = False
        
    def assemble(self, params):
        self.proto.base.seq_num = params.get('seq_num')
        self.is_completely_assembled = True

    def get_bytes(self):
        if False == self.is_completely_assembled:
            raise Exception("Message was not completely assembled.")
        
        msg_bytes = bytearray(struct.pack('H', self.msg_type))
        proto_bytes = self.proto.SerializeToString()
        msg_bytes.extend(bytearray(proto_bytes))
        return msg_bytes
    
    def create_from_bytes(self, msg_bytes):
        this_type = type(self)
        
        if this_type is MessagePingReq:
            self.proto = PingReq()
        elif this_type is MessagePingRsp:
            self.proto = PingRsp()
        elif this_type is MessageText:
            self.proto = Text()
        elif this_type is MessageGoodbye:
            self.proto = Goodbye()
        elif this_type is MessageHello:
            self.proto = Hello()
        else:
            raise Exception("Unknown type for factory.")
        
        msg_str = str(msg_bytes[2:])
        self.proto.ParseFromString(msg_str)
        self.is_completely_assembled = True
        
        
    def accept(self, visitor):
        visitor.visit(self)
        
    def get_seq_num(self):
        return self.proto.base.seq_num

    def get_msg_type(self):
        return self.get_msg_type()


class MessagePingReq(MessageBase):
    '''
    classdocs
    '''
    msg_type = MessageType.PING_REQ
    
    def assemble(self, params):
        self.proto = PingReq()
        super(MessagePingReq, self).assemble(params)
        
        
class MessagePingRsp(MessageBase):
    '''
    classdocs
    '''
    msg_type = MessageType.PING_RSP
    
    def assemble(self, params):
        self.proto = PingRsp()
        self.proto.req_seq_num = params.get('req_seq_num')
        super(MessagePingRsp, self).assemble(params)
        
    def get_req_seq_num(self):
        return self.proto.req_seq_num


class MessageText(MessageBase):
    '''
    classdocs
    '''
    msg_type = MessageType.TEXT
    
    def assemble(self, params):
        self.proto = Text()
        self.proto.msg_txt = params.get('msg_txt')
        super(MessageText, self).assemble(params)
        
    def get_msg_txt(self):
        return self.proto.msg_txt

class MessageGoodbye(MessageBase):
    '''
    classdocs
    '''
    msg_type = MessageType.GOODBYE
    
    def assemble(self, params):
        self.proto = Goodbye()
        self.proto.reason = params.get('reason')
        self.proto.reason_str = params.get('reason_str')
        super(MessageGoodbye, self).assemble(params)
        
    def get_reason(self):
        return self.proto.reason
    
    def get_reason_str(self):
        return self.proto.reason_str
    
class MessageHello(MessageBase):
    '''
    classdocs
    '''
    msg_type = MessageType.HELLO
    
    def assemble(self, params):
        self.proto = Hello()
        self.proto.version = params.get('version')
        super(MessageHello, self).assemble(params)
        
    def get_version(self):
        return self.proto.version