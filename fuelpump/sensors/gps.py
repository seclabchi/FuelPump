'''
Created on Jun 13, 2017

@author: zaremba
'''

import serial
import threading
import Queue
import time
import logging
import binascii

MAX_SENTENCE_Q_SIZE = 64  #if the Q grows past this limit it will be cleared for new data
SENTENCE_GET_WAIT_TIMEOUT = 1.0  #seconds

class Gps(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.rx_buf = bytearray()
        self.sentence_callback = None
        self.device = serial.Serial(baudrate=4800, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        self.connected = False
        self.sentenceQ = Queue.Queue(MAX_SENTENCE_Q_SIZE)
        self.reader_thread = None
        
    def start(self, dev_handle):
        if True == self.connected:
            raise Exception("Already connected to " + self.device.port)
        
        self.device.port = dev_handle
        
        logging.info("Starting GPS device at " + self.device.port + "...")
        self.device.open()
        self.connected = True
        logging.info("GPS at " + self.device.port + " started.")
        start_lock = threading.Lock()
        start_lock.acquire(True)
        logging.debug("Starting reader thread...")
        self.reader_thread = GpsReader(self.device, self.sentenceQ, start_lock)
        self.reader_thread.start()
        start_lock.acquire(True)
        logging.debug("Reader thread started.")
        
    def stop(self):
        if True == self.connected:
            logging.info("Stopping GPS device at " + self.device.port + "...")
            self.reader_thread.stop()
            self.device.close()
            logging.info("GPS at " + self.device.port + " stopped.")
            self.connected = False
            
    def get_sentence(self):
        return self.sentenceQ.get(True, SENTENCE_GET_WAIT_TIMEOUT)
            
            
class GpsReader(threading.Thread):
    '''
    classdocs
    '''
    
    def __init__(self, gps_dev, sentenceQ, start_lock):
        self.sentenceQ = sentenceQ
        self.gps_dev = gps_dev
        self.stop_commanded = False
        self.start_lock = start_lock
        
        self.rx_buf = bytearray()
        self.sentence_in_progress = False
        
        super(GpsReader, self).__init__(None, self.thread_func, "GpsReader")
        
    def stop(self):
        logging.debug("Stopping GpsReader thread...")
        self.stop_commanded = True
        self.join()
        logging.debug("Joined GpsReader thread.")
        
    def thread_func(self):
        logging.debug("GpsReader thread main func started.")
        self.start_lock.release()
        while False == self.stop_commanded:
            logging.debug("GpsReader top of main loop")
            raw_rx = self.gps_dev.read(64)
            self.parse_raw(raw_rx)
            
        logging.debug("GpsReader thread exiting.")
            
    def parse_raw(self, raw):
        for char in raw:
            if False == self.sentence_in_progress:
                if '$' == char:
                    logging.debug("Sentence started.")
                    self.sentence_in_progress = True
                else:
                    logging.debug("Received out of band character " + char)
            else:
                if '\n' == char:
                    logging.debug("Received end of sentence character.")
                    self.sentence_in_progress = False
                    if True == self.checksum_ok():
                        logging.debug("Sentence Q size: " + str(self.sentenceQ.qsize()))
                        if self.sentenceQ.full():
                            logging.warn("GPS RX Sentence Q full...clearing.")
                            with self.sentenceQ.mutex:
                                self.sentenceQ.queue.clear()
                        self.sentenceQ.put_nowait(str(self.rx_buf))
                    self.rx_buf = bytearray()
                elif '\r' == char:
                    pass #don't care, ignore it
                else:
                    self.rx_buf.append(char)
            
    def checksum_ok(self):
        csok = False
        computed_cs = 0x00
        received_cs_str = self.rx_buf[-2:]
        received_cs = ord(binascii.unhexlify(received_cs_str))
        
        self.rx_buf = self.rx_buf[:-3]
        
        for char in self.rx_buf:
            computed_cs = computed_cs ^ char
            
        if computed_cs == received_cs:
            logging.debug("Checksum OK")
            csok = True
        else:
            received_cs_hex = hex(received_cs)
            computed_cs_hex = hex(computed_cs)
            logging.error("BAD CHECKSUM - Received checksum " + received_cs_hex + " != computed " + computed_cs_hex)
    
        return csok

if __name__ == '__main__':
    pass