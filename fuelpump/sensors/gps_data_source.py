'''
Created on Jun 14, 2017

@author: zaremba
'''

import threading
import logging
import time
from fuelpump.sensors.gps import Gps

class GpsDataSource(object):
    '''
    classdocs
    '''

    def __init__(self, gps, dev_handle):
        self.gps = gps
        self.gps_dev_handle = dev_handle
        self.reader = GpsSentenceReader(self.gps, self)
        
    def start(self):
        self.gps.start(self.gps_dev_handle)
        self.reader.start()
        
    def stop(self):
        self.reader.stop()
        self.gps.stop()
        
    
class GpsSentenceReader(threading.Thread):
    '''
    classdocs
    '''
    
    def __init__(self, gps, controller):
        self.gps = gps
        self.controller = controller
        self.shutdown_signalled = False
        super(GpsSentenceReader, self).__init__(None, self.run_func, "GpsSentenceReader")
        
    def stop(self):
        self.shutdown_signalled = True
        self.join()
            
    def run_func(self):
        while False == self.shutdown_signalled:
            sentence = self.gps.get_sentence()
            parts = sentence.split(",")
            logging.debug("Got sentence type " + parts[0])
            
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging_stream_handler = logging.StreamHandler()
    logging.Formatter.converter = time.gmtime
    log_formatter = logging.Formatter("%(asctime)s [%(filename)-20.20s:%(lineno)-4.4s - %(funcName)-25.25s] [%(threadName)-18.18s] [%(levelname)-5.5s]  %(message)s")
    logging_stream_handler.setFormatter(log_formatter)
    logging.getLogger().addHandler(logging_stream_handler)
    gps = Gps()
    data_source = GpsDataSource(gps, '/dev/tty.usbserial4')
    data_source.start()
    time.sleep(10)
    data_source.stop()
    