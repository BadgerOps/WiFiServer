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

    def _setup(self):
        pass

    def get_networks(self):
        '''get a list of networks...'''
        interface = 'wlan0'  #FIXME:  shouldn't be hardcoded
        return Cell.all(interface)

    def dict_networks(self, network_list):
        '''build a dictionary object out of network information'''
        ap = {}
        nw = {}
        for item in network_list:
            nw['network'] = item.ssid
            nw['encrypted'] = item.encrypted
            nw['encryption'] = item.encryption_type
            nw['mac_addr'] = item.address
            ap['network'] = nw
        return ap

    def list_networks(self):
        if len(self.networks) > 0:
            return self.dict_networks(self.networks)
        else:
            self.networks = self.get_networks()
            return self.dict_networks(self.networks)
