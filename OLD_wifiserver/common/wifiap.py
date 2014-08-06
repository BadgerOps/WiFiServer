#!/usr/bin/env python

import os
import logging
from svc import WiFiObj
from time import sleep
from managedhcp import ManageDHCP


class WiFiAP(WiFiObj):
    """
    Allows creation and management of WiFi AP on compatible wireless cards
    Requires hostapd, dnsmasq
    """
    def __init__(self):
        self.dhcp = ManageDHCP()

    def run(self):
        while self.svc.apmode is True:
            self.startap()
        self.stopap()

    def startap(self):
        logging.info("Starting WiFi AP")
        self.dhcp.start()
        try:
            os.system('sudo nmcli nm wifi off')  # TODO: don't want to rely on network-manager
            os.system('sudo rfkill unblock wlan0')  # Remove possible WLAN block
            os.system('sudo ifconfig wlan0 10.15.0.1/24 up')
        except Exception as e:
            logging.warning('Unable to prepare WiFi AP interface: {}'.format(e))
        try:
            os.system('sudo service hostapd start')
        except Exception as e:
            logging.critical("Unable to start WiFi AP: {}".format(e))

    def stopap(self):
        logging.info("Stopping WiFi AP")
        self.dhcp.stop()
        try:
            os.system('sudo service hostapd stop')
        except Exception as e:
            logging.critical("Unable to stop WiFi AP: {}".format(e))
        finally:
            os.system('sudo nmcli nm wifi on')
