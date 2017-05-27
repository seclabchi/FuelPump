'''
Created on May 27, 2017

@author: zaremba
'''

class ClientConnectionRegistry(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.client_list = []
        
    def add(self, client):
        self.client_list.append(client)
        
    def get_clients(self):
        return self.client_list
        
    def remove(self, client):
        print "Removing client " + repr(client.addr)