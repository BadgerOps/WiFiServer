#!/usr/bin/env python


from wifi import Cell, Scheme
import time
import logging
import os
import sys
import configparser
from time import sleep


class WifiClient(object):

    def __init__(self):
        self.networks = []
        #self._setup()
        self.interface = 'wlan0'  # TODO: move this to cfg

    def _setup(self):
        pass

    @property
    def scan(self):
        '''
        wrapper for the web restful endpoint
        :rtype : dictionary
        '''
        return self.dict_networks(self.get_networks())

    def get_networks(self):
        '''get a list of networks...'''
        return Cell.all(self.interface)

    def dict_networks(self, network_list):
        '''build a dictionary object out of network information
        :rtype : dictionary
        '''
        ap = {}
        nw = {}
        for item in network_list:
            nw['network'] = item.ssid
            nw['encrypted'] = item.encrypted
            nw['encryption'] = item.encryption_type
            nw['mac_addr'] = item.address
            ap[nw['network']] = nw
        return ap

    def list_networks(self):
        if len(self.networks) > 0:
            return self.dict_networks(self.networks)
        else:
            self.networks = self.get_networks()
            return self.dict_networks(self.networks)
