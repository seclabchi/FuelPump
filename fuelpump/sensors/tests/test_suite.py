'''
Created on Jun 14, 2017

@author: zaremba
'''

import unittest
import time
import logging
from fuelpump.sensors.tests import *

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging_stream_handler = logging.StreamHandler()
    logging.Formatter.converter = time.gmtime
    log_formatter = logging.Formatter("%(asctime)s [%(filename)-20.20s:%(lineno)-4.4s - %(funcName)-25.25s] [%(threadName)-18.18s] [%(levelname)-5.5s]  %(message)s")
    logging_stream_handler.setFormatter(log_formatter)
    logging.getLogger().addHandler(logging_stream_handler)
    
    suite = unittest.TestLoader().loadTestsFromName('gps_tests')
    unittest.TextTestRunner(verbosity=3).run(suite)
    