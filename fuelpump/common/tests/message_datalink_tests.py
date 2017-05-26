'''
Created on May 25, 2017

@author: zaremba
'''
import unittest
import binascii
from fuelpump.common.message_factory import MessageFactory
from fuelpump.common.message_datalink import MessageDatalink


class MessageDatalinkTests(unittest.TestCase):

    def print_enc(self, msg):
        enc_bytes = MessageDatalink.encode(msg)
        print binascii.hexlify(enc_bytes)

    def test_encode(self):
        msg = MessageFactory.get_ping_req()
        self.print_enc(msg)
        
        msg = MessageFactory.get_ping_rsp(23)
        self.print_enc(msg)
        
        msg = MessageFactory.get_text("Hello from the \x10 MessageDatalinkTests test_encode test!!!\x10\x10")
        self.print_enc(msg)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()