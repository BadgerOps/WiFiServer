#!/usr/bin/env python

import logging
import os
import sys
import configparser
from managedhcp import ManageDHCP
from time import sleep


class WiFiAP():
    """
    Allows creation of WiFi AP on compatible wireless cards
    Requires hostapd and dnsmasq
    """
    def __init__(self):
      self.set_logging()

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
        ManageDHCP.start()
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
            ManageDHCP.stop()
        except Exception as e:
            logging.warning('Unable to stop services: {}'.format(e))
        else:
            os.system('sudo nmcli nm wifi on')

    def set_logging(self):  # todo: logging should be set by master, location from cfg
        """
        Enables logging
        """
        logging.basicConfig(filename='/var/log/wifiap.log', level=logging.DEBUG)

if __name__ == "__main__":
    WiFiAP.start_ap()
    sleep(60)
    WiFiAP.stop_all()
