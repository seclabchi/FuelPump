'''
Created on Jun 14, 2017

@author: zaremba
'''

import threading
import logging
import time
from fuelpump.sensors.gps import Gps
from fuelpump.sensors.nmea_data import *

class GpsDataSource(object):
    '''
    classdocs
    '''

    def __init__(self, gps, dev_handle):
        self.gps = gps
        self.gps_dev_handle = dev_handle
        self.reader = GpsSentenceReader(self.gps, self)
        self.svs = []
        self.gprmc = None
        self.gpgsa = None
        self.gpgga = None
        
        self.lock_gpgsv = threading.Lock()
        self.lock_gprmc = threading.Lock()
        self.lock_gpgsa = threading.Lock()
        self.lock_gpgga = threading.Lock()
        
    def start(self):
        self.gps.start(self.gps_dev_handle)
        self.reader.start()
        
    def stop(self):
        self.reader.stop()
        self.gps.stop()
        
    def set_GPRMC_data(self, time, nav_rcvr_warning, lat, lat_ns, lon, lon_ew, spd_kts, crs_true, date, mag_var, mag_var_ew):
        self.lock_gprmc.acquire()
        self.gprmc = GPRMCData()
        self.gprmc.init_from_string_params(time, nav_rcvr_warning, lat, lat_ns, lon, lon_ew, spd_kts, crs_true, date, mag_var, mag_var_ew)
        self.lock_gprmc.release()
        
    def get_GPRMC_data(self):
        rmc = GPRMCData()
        self.lock_gprmc.acquire()
        gprmc = GPRMCData()
        if None != self.gprmc:
            gprmc.init_by_copy(self.gprmc)
        self.lock_gprmc.release()
        return gprmc
        
    def set_GPGSA_data(self, mode_op, mode_fix, fix_svs, pdop, hdop, vdop):
        self.lock_gpgsa.acquire()
        self.gpgsa = GPGSAData()
        self.gpgsa.init_from_string_params(mode_op, mode_fix, fix_svs, pdop, hdop, vdop)
        self.lock_gpgsa.release()
    
    def get_GPGSA_data(self):
        gsa = GPGSAData()
        self.lock_gpgsa.acquire()
        if None != self.gpgsa:
            gsa.init_by_copy(self.gpgsa)
        self.lock_gpgsa.release()
        return gsa
    
    def set_GPGGA_data(self):
        pass
    
    def set_GPGSV_data(self, svs):
        self.lock_gpgsv.acquire()
        logging.debug("Setting data source SVs to a new batch of " + str(len(svs)) + " SVs.")
        self.svs = []
        for sv in svs:
            self.svs.append(sv)
            if sv.snr == '':
                logging.debug("SV " + str(sv.prn) + " NOT TRACKED.")
        self.lock_gpgsv.release()
            
    def get_GPGSV_data(self):
        svs = []
        self.lock_gpgsv.acquire()
        for sv in self.svs:
            svs.append(sv)
        self.lock_gpgsv.release()
        return svs
    
class GpsSentenceReader(threading.Thread):
    '''
    classdocs
    '''
    
    def __init__(self, gps, controller):
        self.gps = gps
        self.controller = controller
        self.shutdown_signalled = False
        self.svs = []
        self.sv_count = 0
        super(GpsSentenceReader, self).__init__(None, self.run_func, "GpsSentenceReader")
        
    def stop(self):
        self.shutdown_signalled = True
        self.join()
            
    def run_func(self):
        while False == self.shutdown_signalled:
            sentence = self.gps.get_sentence()
            logging.debug("FULL SENTENCE " + sentence)
            parts = sentence.split(",")
            logging.debug("Got sentence type " + parts[0])
            
            if 'GPGSV' == parts[0]:
                if '1' == parts[2]:
                    self.svs = []
                    self.sv_count = int(parts[3])
                
                for i in range(4, len(parts), 4):
                    sv_data_tuple = tuple(parts[i:i+4])
                    sv = SV(sv_data_tuple)
                    self.svs.append(sv)
                    logging.debug("SV DATA:" + sv.prn + " " + sv.elev + " " + sv.azi + " " + sv.snr)
                    if len(self.svs) == self.sv_count:
                        self.controller.set_GPGSV_data(self.svs)
                        
            elif 'GPRMC' == parts[0]:
                self.controller.set_GPRMC_data(parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7], parts[8], parts[9], parts[10], parts[11])
            elif 'GPGSA' == parts[0]:
                self.controller.set_GPGSA_data(parts[1], parts[2], (parts[3], parts[4], parts[5], parts[6], parts[7], parts[8], parts[9], parts[10], parts[11], parts[12], parts[13], parts[14]), parts[15], parts[16], parts[17])
            elif 'GPGGA' == parts[0]:
                self.controller.set_GPGGA_data()
            else:
                logging.warn("Received unknown NMEA sentence type " + parts[0])
            
                
                
            
            
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    logging_stream_handler = logging.StreamHandler()
    logging.Formatter.converter = time.gmtime
    log_formatter = logging.Formatter("%(asctime)s [%(filename)-20.20s:%(lineno)-4.4s - %(funcName)-25.25s] [%(threadName)-18.18s] [%(levelname)-5.5s]  %(message)s")
    logging_stream_handler.setFormatter(log_formatter)
    logging.getLogger().addHandler(logging_stream_handler)
    gps = Gps()
    data_source = GpsDataSource(gps, '/dev/tty.usbserial4')
    data_source.start()
    run_count = 0
    
    while run_count < 10:
        svs = data_source.get_GPGSV_data()
        for sv in svs:
            print repr(sv.get_tuple()) + " | ",
        print ''
        rmc = data_source.get_GPRMC_data()
        print repr(rmc.get_tuple())
        gsa = data_source.get_GPGSA_data()
        print repr(gsa.get_tuple())
        run_count = run_count + 1
        time.sleep(2)
    data_source.stop()
    