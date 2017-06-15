'''
Created on Jun 13, 2017

@author: zaremba
'''
import unittest
import serial
import logging
from fuelpump.sensors.gps import *

GPS_DEV_HANDLE = "/dev/tty.usbserial4"

class GpsTest(unittest.TestCase):

    def setUp(self):
        print "Test setUp"
        self.gps = Gps()
        
    def tearDown(self):
        print "Test tearDown"
        if(None != self.gps):
            self.gps.stop()
            self.gps = None

    def testBadOpen(self):        
        with self.assertRaises(serial.SerialException) as context:
            self.gps.start("doesn't exist")
        print "Successfully caught SerialException for bad device handle."
              
    def testGoodOpenClose(self):
        self.gps.start(GPS_DEV_HANDLE)
        self.gps.stop()
        
    def testReopen(self):
        self.gps.start(GPS_DEV_HANDLE)
        
        with self.assertRaises(Exception) as context:
            self.gps.start(GPS_DEV_HANDLE)
        print "Successfully caught exception trying to reopen GPS device."
            
    def testReadSomeData(self):
        self.gps.start(GPS_DEV_HANDLE)
        time.sleep(5)
                    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()