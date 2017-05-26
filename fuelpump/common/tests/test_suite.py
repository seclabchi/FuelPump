'''
Created on May 23, 2017

@author: zaremba
'''

import unittest
from fuelpump.common.tests import *

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromNames(('message_tests', 'message_factory_tests', 'message_datalink_tests'))
    unittest.TextTestRunner(verbosity=3).run(suite)
    