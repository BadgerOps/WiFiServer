#!/usr/bin/env python

import logging
import os
import sys
import configparser
from time import sleep


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
        config.read(cfg_file)
        config.set('default', )

    def set_logging(self):
        """
        Enables logging
        """
        logging.basicConfig(filename='/var/log/pifi.log', level=logging.DEBUG)

if __name__ == "__main__":
    arg = sys.argv[1]
    WifiAP(arg)