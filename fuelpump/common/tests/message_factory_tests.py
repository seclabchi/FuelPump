'''
Created on May 23, 2017

@author: zaremba
'''
import unittest
from fuelpump.common.message import *
from fuelpump.common.message_factory import *

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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()