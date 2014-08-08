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

    def scan(self):
        '''
        wrapper for the web restful endpoint
        :rtype : dictionary
        '''
        return self.dict_networks(self.get_networks())

    def join_network(self, data):
        cell = self.networks[data['network']]
        scheme = Scheme.for_cell(self.interface, data['name'], cell, data['passkey'])
        scheme.activate()

    def add_network(self, data):
        """add a new network config"""
        if self.verify_network(data['name']):
            self.join_network(data)
        else:
            logging.warn("sorry, I cant see that network to add it")

    def save_network(self, data):
        pass

    def verify_network(self, name):
        """check to make sure we know about the network"""
        if name in self.networks:
            return True
        else:  # try one more time
            self.networks = self.get_networks()
            if name in self.networks:
                return True
            else:
                return False

    def get_networks(self):
        '''get a list of networks...'''
        return Cell.all(self.interface)

    def dict_networks(self, network_list):
        """
        build a dictionary object out of network information
        :rtype : dictionary
        """
        ap = {}
        nw = {}
        for item in network_list:
            nw['network'] = item.ssid
            nw['encrypted'] = item.encrypted
            nw['encryption'] = item.encryption_type
            nw['mac_addr'] = item.address
            ap[nw['network']] = nw  # build a dictionary with the ssid as the key
        return ap

    def list_networks(self):
        if len(self.networks) > 0:
            return self.dict_networks(self.networks)
        else:
            self.networks = self.get_networks()
            return self.dict_networks(self.networks)
