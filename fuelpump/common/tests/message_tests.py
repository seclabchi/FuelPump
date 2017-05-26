'''
Created on May 20, 2017

@author: zaremba
'''
import unittest
from fuelpump.common.message import *
import binascii

class TestVisitor(object):
    def visit(self, visited_msg):
        print "Visitor received " + MessageType.str_from_type(visited_msg.msg_type)

class MessageTests(unittest.TestCase):
    
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testVisitor(self):
        visitor = TestVisitor()
        
        msg_ping = MessagePingReq()
        msg_ping.assemble({'seq_num': 1})
        msg_text = MessageText()
        msg_text.assemble({'seq_num': 2, 'msg_txt': 'Hello, world!'})
        
        msgs = [msg_ping, msg_text]
        
        for obj in msgs:
            obj.accept(visitor)
        
        
    def testTypeDecoder(self):
        msg_type_str = MessageType.str_from_type(9999)
        self.assertEqual("NONE", msg_type_str)
        
        
    def testInstantiateBase(self):
        with self.assertRaises(Exception):
            msg_bad = MessageBase({})
            
    def testPingGetBytes(self):
        msg_ping = MessagePingReq()
        msg_ping.assemble({'seq_num':232323})
        self.msg_bytes = msg_ping.get_bytes()
        print binascii.hexlify(self.msg_bytes)
        
    def testPingReqCreateFromBytes(self):
        msg_ping = MessagePingReq()
        msg_ping.assemble({'seq_num':232323})
        msg_bytes = msg_ping.get_bytes()
        print binascii.hexlify(msg_bytes)
        
        msg_ping2 = MessagePingReq()
        msg_ping2.create_from_bytes(msg_bytes)
        
    def testPingReqEncodeDecode(self):
        msg = PingReq()
        msg.base.seq_num = 232323
        
        msg_str = msg.SerializeToString()
        
        msg2 = PingReq()
        msg2.ParseFromString(msg_str)
        pass
    
    def testPingRspLocalRoundTrip(self):
        msg = MessagePingRsp()
        msg_seq_num = 99887766
        msg.assemble({'seq_num':msg_seq_num, 'req_seq_num':42})
        msg_bytes = msg.get_bytes()
        print binascii.hexlify(msg_bytes)
        
        msg2 = MessagePingRsp()
        msg2.create_from_bytes(msg_bytes)
        
        msg_seq_num_check = msg2.get_seq_num()
        
        self.assertEqual(msg_seq_num, msg_seq_num_check)
        
    def testTextLocalRoundTrip(self):
        msg = MessageText()
        msg_str = "Hello, Protobufs, and Hello SecretLabComms in Python!!!"
        msg_seq_num = 12345678
        msg.assemble({'seq_num':msg_seq_num, 'msg_txt':msg_str})
        msg_bytes = msg.get_bytes()
        print binascii.hexlify(msg_bytes)
        
        msg2 = MessageText()
        msg2.create_from_bytes(msg_bytes)
        
        msg_seq_num_check = msg2.get_seq_num()
        msg_str_check = msg2.get_msg_txt()
        
        self.assertEqual(msg_str, msg_str_check)
        self.assertEqual(msg_seq_num, msg_seq_num_check)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    