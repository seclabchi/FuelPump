'''
Created on May 25, 2017

@author: zaremba
'''
import unittest
from fuelpump.common.message_factory import MessageFactory
from fuelpump.common.message_datalink import MessageDatalink


class MessageDatalinkTests(unittest.TestCase):


    def test_encode(self):
        msg = MessageFactory.get_ping_req()
        MessageDatalink.encode(msg)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()