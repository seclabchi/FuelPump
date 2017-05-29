'''
Created on May 23, 2017

@author: zaremba
'''
import unittest
from fuelpump.common.message import *
from fuelpump.common.message_factory import *
from fuelpump.common.messages_pb2 import *

class MessageFactoryTests(unittest.TestCase):

    def testGetPingReq(self):
        msg = MessageFactory.get_ping_req()
         
        self.assertEqual(type(msg).__name__, 'MessagePingReq')
        print str(msg.proto)
        
    def testGetPingRsp(self):
        msg = MessageFactory.get_ping_rsp(23)
        
        self.assertEqual(type(msg).__name__, 'MessagePingRsp')
        self.assertEqual(msg.get_req_seq_num(), 23)
        print str(msg.proto)
        
    def testGetText(self):
        text_input_msg = "Hello, world, from the Unit Test Python World!"
        msg = MessageFactory.get_text(text_input_msg)
        
        self.assertEqual(type(msg).__name__, 'MessageText')
        self.assertEqual(msg.get_msg_txt(), text_input_msg)
        print str(msg.proto)
        
    def testGetGoodbye(self):
        reason = Goodbye.SERVER_SHUTDOWN_NORMAL
        reason_str = "Unit test server is shutting down."
        
        msg = MessageFactory.get_goodbye(reason, reason_str)
        
        self.assertEqual(type(msg).__name__, 'MessageGoodbye')
        self.assertEqual(msg.get_reason(), Goodbye.SERVER_SHUTDOWN_NORMAL)
        self.assertEqual(msg.get_reason_str(), reason_str)
        
        print str(msg.proto)
        
    def testGetHello(self):
        version = 12345678
        msg = MessageFactory.get_hello(version)
        
        self.assertEqual(type(msg).__name__, 'MessageHello')
        self.assertEqual(msg.get_version(), version)
        
        print str(msg.proto)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()