#!/usr/bin/env python

import RPi.GPIO as gpio
from wifi import Cell, Scheme
import time

class OctoWifi(object):

    def __init__(self):
        self.networks = []
        self._setup()
        self.gpio_pin = 26

    def _setup(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.gpio_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

    def get_networks(self):
        '''get a list of networks...'''
        interface = 'wlan0'
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

        print ap

    def list_networks(self):
        if len(self.networks) > 0:
            return self.networks
        else:
            self.networks = self.get_networks()
            return self.networks

    def run(self):
        while True:
            print self.list_networks()
            print self.gpio_stuff()
            time.sleep(10)

    def gpio_check(self):
        if (gpio.input(self.gpio_pin) == 0):
            return True
        else:
            return False


if __name__ == '__main__':
    #print 'this is a module, dont run it on its own'
    ow = OctoWifi()
    ow.run()
