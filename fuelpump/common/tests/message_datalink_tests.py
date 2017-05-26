'''
Created on May 25, 2017

@author: zaremba
'''
import unittest
import binascii
from fuelpump.common.message_factory import MessageFactory
from fuelpump.common.message_datalink import MessageDatalink


class MessageDatalinkTests(unittest.TestCase):
        
    def __init__(self, *args, **kwargs):
        self.message_reference = None
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
        
    def test_local_decode_ping_req(self):
        test_msg_source = MessageFactory.get_ping_req()
        self.message_reference = test_msg_source.get_bytes()
        
        enc_msg = MessageDatalink.encode(test_msg_source)
        
        datalink = MessageDatalink()
        datalink.decode(enc_msg, self.decode_callback)
        
    def test_local_decode_text(self):
        test_msg_source = MessageFactory.get_text("Hello \x10 \x10 \x02 \x03 from the purposefully \x03 \x02 \x10 weirdly-crafted text message datalink test.")
        self.message_reference = test_msg_source.get_bytes()
        enc_msg = MessageDatalink.encode(test_msg_source)
        
        datalink = MessageDatalink()
        datalink.decode(enc_msg, self.decode_callback)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()