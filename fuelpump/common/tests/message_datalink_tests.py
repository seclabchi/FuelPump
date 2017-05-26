'''
Created on May 25, 2017

@author: zaremba
'''
import unittest
import binascii
from fuelpump.common.message_factory import MessageFactory
from fuelpump.common.message_datalink import MessageDatalink


class MessageDatalinkTests(unittest.TestCase):
    
    message_reference = None
    
    def __init__(self, *args, **kwargs):
        super(MessageDatalinkTests, self).__init__(*args, **kwargs)

    def print_enc(self, msg):
        enc_bytes = MessageDatalink.encode(msg)
        print binascii.hexlify(enc_bytes)
        
    def decode_callback(self, bytes):
        decoded_message = bytes
        self.assertEqual(decoded_message[4:], self.message_reference)

    def test_encode(self):
        msg = MessageFactory.get_ping_req()
        self.print_enc(msg)
        
        msg = MessageFactory.get_ping_rsp(23)
        self.print_enc(msg)
        
        msg = MessageFactory.get_text("Hello from the \x10 MessageDatalinkTests test_encode test!!!\x10\x10")
        self.print_enc(msg)
        
    def test_local_decode(self):
        test_msg_source = MessageFactory.get_ping_req()
        self.message_reference = test_msg_source.get_bytes()
        
        enc_msg = MessageDatalink.encode(test_msg_source)
        
        datalink = MessageDatalink()
        decoded_msg = datalink.decode(enc_msg, self.decode_callback)
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()