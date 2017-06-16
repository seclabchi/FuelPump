'''
Created on Jun 14, 2017

@author: zaremba
'''

import logging
import collections
import copy

def pos_str_to_float(pos, dir):
    pass

class SV(object):
    '''
    classdocs
    '''
    NamedTuple = collections.namedtuple('SV', ['prn', 'elev', 'azi', 'snr'])
    
    def __init__(self, sv_data_tuple):
        self.prn = sv_data_tuple[0]
        self.elev = sv_data_tuple[1]
        self.azi = sv_data_tuple[2]
        self.snr = sv_data_tuple[3]
        
    def __str__(self):
        return "SV PRN " + self.prn + ", elevation " + self.elev + ", azimuth " + self.azi + ", SNR " + self.snr
    
    def get_tuple(self):
        return self.NamedTuple(self.prn, self.elev, self.azi, self.snr)
        
class GPRMCData(object):
    '''
    classdocs
    '''
    
    NamedTuple = collections.namedtuple('GPRMCData', ['time', 'nav_rcvr_warning', 'lat', 'lat_ns', 'lon', 'lon_ew', 'spd_kts', 'crs_true', 'date', 'mag_var', 'mag_var_ew'])
    
    def __init__(self):
        self.time = ''
        self.nav_rcvr_warning = ''
        self.lat = 0.0
        self.lat_ns = ''
        self.lon = 0.0
        self.lon_ew = ''
        self.spd_kts = 0.0
        self.crs_true = 0.0
        self.date = ''
        self.mag_var = 0.0
        self.mag_var_ew = ''
        
    def init_from_string_params(self, time, nav_rcvr_warning, lat, lat_ns, lon, lon_ew, spd_kts, crs_true, date, mag_var, mag_var_ew):
        self.time = time
        self.nav_rcvr_warning = nav_rcvr_warning
        self.lat = pos_str_to_float(lat, lat_ns)
        self.lat_ns = lat_ns
        self.lon = pos_str_to_float(lon, lon_ew)
        self.lon_ew = lon_ew
        self.spd_kts = float(spd_kts)
        self.crs_true = float(crs_true)
        self.date = date
        if '' != mag_var:
            self.mag_var = float(mag_var)
        self.mag_var_ew = mag_var_ew
        
    def init_by_copy(self, rhs):
        self.time = rhs.time
        self.nav_rcvr_warning = rhs.nav_rcvr_warning
        self.lat = rhs.lat
        self.lat_ns = rhs.lat_ns
        self.lon = rhs.lon
        self.lon_ew = rhs.lon_ew
        self.spd_kts = rhs.spd_kts
        self.crs_true = rhs.crs_true
        self.date = rhs.date
        self.mag_var = rhs.mag_var
        self.mag_var_ew = rhs.mag_var_ew
        
    def get_tuple(self):
        gprmc_data = self.NamedTuple(self.time, self.nav_rcvr_warning, self.lat, self.lat_ns, self.lon, self.lon_ew, self.spd_kts, self.crs_true, self.date, self.mag_var, self.mag_var_ew)
        return gprmc_data 
    
    
class GPGGAData(object):  #not sure if needed...table this
    '''
    classdocs
    '''
    NamedTuple = collections.namedtuple('GPGGAData', [])


class GPGSAData(object):
    '''
    classdocs
    '''
    NamedTuple = collections.namedtuple('GPGSAData', ['mode_op', 'mode_fix', 'sv_list', 'pdop', 'hdop', 'vdop'])
    
    def __init__(self):
        self.mode_op = ''
        self.mode_fix = 1
        self.sv_list = []
        self.pdop = 0.0
        self.hdop = 0.0
        self.vdop = 0.0
        
    def init_from_string_params(self, mode_op, mode_fix, sv_list, pdop, hdop, vdop):
        self.mode_op = mode_op
        self.mode_fix = int(mode_fix)
        for sv in sv_list:
            if '' != sv:
                self.sv_list.append(sv)
        self.pdop = float(pdop)
        self.hdop = float(hdop)
        self.vdop = float(vdop)
        
    def init_by_copy(self, rhs):
        self.mode_op = rhs.mode_op
        self.mode_fix = rhs.mode_fix
        self.sv_list = copy.deepcopy(rhs.sv_list)
        self.pdop = rhs.pdop
        self.hdop = rhs.hdop
        self.vdop = rhs.vdop
        
    def get_tuple(self):
        return self.NamedTuple(self.mode_op, self.mode_fix, copy.deepcopy(self.sv_list), self.pdop, self.hdop, self.vdop)