'''
Created on Jun 14, 2017

@author: zaremba
'''

import logging

class SV(object):
    '''
    classdocs
    '''
    def __init__(self, sv_data_tuple):
        self.prn = sv_data_tuple[0]
        self.elev = sv_data_tuple[1]
        self.azi = sv_data_tuple[2]
        self.snr = sv_data_tuple[3]
        
    def __str__(self):
        return "SV PRN " + self.prn + ", elevation " + self.elev + ", azimuth " + self.azi + ", SNR " + self.snr
        
class RMCData(object):
    '''
    classdocs
    '''
    def __init__(self, rmc_data_tuple):
        self.time_str = rmc_data_tuple[0]
        self.nav_rcvr_warning = rmc_data_tuple[1]
        self.lat_str = rmc_data_tuple[2]
        self.lat_str_ns = rmc_data_tuple[3]
        self.lon_str = rmc_data_tuple[4]
        self.lon_str_ew = rmc_data_tuple[5]
        self.spd_kts_str = rmc_data_tuple[6]
        self.crs_true_str = rmc_data_tuple[7]
        self.date_str = rmc_data_tuple[8]
        self.mag_var_str = rmc_data_tuple[9]
        self.mag_var_ew_str = rmc_data_tuple[10]
        
    def get_tuple(self):
        return (self.time_str, self.nav_rcvr_warning, self.lat_str, self.lat_str_ns, self.lon_str, self.lon_str_ew, self.spd_kts_str, self.crs_true_str, self.date_str, self.mag_var_str, self.mag_var_ew_str)
    
    def __str__(self):
        return "GPRMC: " + self.time_str + ", " + self.nav_rcvr_warning + ", " + self.lat_str + ", " + self.lat_str_ns + ", " + self.lon_str + ", " + self.lon_str_ew + ", " + self.spd_kts_str + ", " + self.crs_true_str + ", " + self.date_str + ", " + self.mag_var_str + ", " + self.mag_var_ew_str
    