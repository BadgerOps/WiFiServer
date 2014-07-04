#!/usr/bin/env python


from wifi import Cell, Scheme
import time
import logging
import os
import sys
import configparser
from time import sleep
try:
    import RPi.GPIO as gpio
except Exception:
    print 'cannot import the RPi.GPIO lib, is it installed?'

class OctoWifi(object):

    def __init__(self):
        self.networks = []
        self._setup()
        #self.gpio_pin = 26

    def _setup(self):
        pass
        # gpio.setmode(gpio.BOARD)
        # gpio.setup(self.gpio_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

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

        print ap

    def list_networks(self):
        if len(self.networks) > 0:
            return self.dict_networks(self.networks)
        else:
            self.networks = self.get_networks()
            return self.dict_networks(self.networks)

    def run(self):
        while True:
            print self.list_networks()
            #print self.gpio_stuff()
            time.sleep(10)

    def gpio_check(self):
        if (gpio.input(self.gpio_pin) == 0):
            return True
        else:
            return False



class WifiAP():
    """
    Allows creation of WiFi AP on compatible wireless cards
    Requires hostapd and dnsmasq
    """
    def __init__(self, arg):
        if arg == 'start':
            self.start_ap()
        elif arg == 'stop':
            self.stop_all()

    def start_ap(self):
        """
        Starts an access point
        """
        try:
            os.system('sudo nmcli nm wifi off')  # Turn WiFi off
            os.system('sudo rfkill unblock wlan')  # Remove possible WLAN block
            os.system('sudo ifconfig wlan0 10.15.0.1/24 up')
        except Exception as e:
            logging.warning('Unable to prepare interface: {}'.format(e))
        sleep(2)
        self.start_dhcp()
        try:
            os.system('sudo service hostapd start')
        except Exception as e:
            logging.warning('Unable to start hostapd: {}'.format(e))

    def start_dhcp(self):
        """
        Starts DHCP server
        """
        try:
            os.system('sudo service dnsmasq start')
        except Exception as e:
            logging.warning('Unable to start DNS: {}'.format(e))

    def stop_all(self):
        """
        Closes AP and DHCP server, restarts regular networking
        """
        try:
            os.system('sudo service hostapd stop')
            os.system('sudo service dnsmasq stop')
        except Exception as e:
            logging.warning('Unable to stop services: {}'.format(e))
        else:
            os.system('sudo nmcli nm wifi on')

    def build_config(self, cfg):
        """
        Sets configuration for hostapd & dnsmasq
        """
        if cfg == 'hostapd':
            cfg_path = '/etc/hostapd/hostapd.conf'
        elif cfg == 'dnsmasq':
            cfg_path = '/etc/dnsmasq.conf'
        else:
            logging.warning('Unknown cfg type: {}'.format(cfg))

        return cfg_path

    def write_config(self, cfg_path):
        """
        Writes configs to configfiles
        """
        config = configparser.RawConfigParser()
        config.read(cfg_path)
        config.set('default', )

    def set_logging(self):
        """
        Enables logging
        """
        logging.basicConfig(filename='/var/log/pifi.log', level=logging.DEBUG)
