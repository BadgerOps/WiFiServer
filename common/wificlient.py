#!/usr/bin/env python


from wifi import Cell, Scheme
import time
import logging
import os
import sys
import configparser
from time import sleep


class WifiClient(object):
    def __init__(self, wifiserver):
        self.wifiserver = wifiserver
        self.networks = []
        #self._setup()
        self.interface = 'wlan0'  # TODO: move this to cfg

    def _setup(self):
        """
        set up initial configuration
        """
        pass

    def scan(self):
        '''
        wrapper for the web restful endpoint
        :rtype : dictionary
        '''
        return self.dict_networks(self.get_networks())

    def join_network(self, data):
        cell = [x for x in self.networks if x.ssid == data['name']][0]
        conn = Scheme.for_cell(self.interface, data['name'], cell, data['passkey'])
        self.wifiserver.svc.apmode = False
        while self.wifiserver.svc.ap_active:
            logging.debug("Waiting for AP to shut down")
            sleep(1)
        logging.debug("Activating Wireless connection")
        conn.activate()
        return {'join': 'successful'}  # FIXME: return something more meaningful

    def add_network(self, data):
        """add a new network config"""
        if self.verify_network(data['name']):
            self.join_network(data)
        else:
            logging.warn("sorry, I can't see that network to add it")

    def save_network(self, data):
        """save network to config file"""
        cell = [x for x in self.networks if x.ssid == data['name']][0]
        conn = Scheme.for_cell(self.interface, data['name'], cell, data['passkey'])
        conn.save()
        logging.info('saved network {}'.format(data['name']))

    def verify_network(self, name):
        """check to make sure we know about the network"""
        if name in [x.ssid for x in self.networks]:
            return True
        else:  # try one more time
            self.networks = self.get_networks()
            if name in [x.ssid for x in self.networks]:
                return True
            else:
                return False

    def get_networks(self):
        '''get a list of networks...'''
        networks = Cell.all(self.interface)
        if networks:
            return networks
        else:
            logging.warn("Unable to find networks - Interface {}".format(self.interface))
            return []

    def dict_networks(self, network_list):
        """
        build a dictionary object out of network information
        :rtype : dictionary
        """
        ap = {}
        for item in network_list:
            nw = {}
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
