#!/usr/bin/env python

import os
import logging
from common.svc import WiFiObj
from managedhcp import ManageDHCP


class WiFiAP(WiFiObj):
    """
    Allows creation and management of WiFi AP on compatible wireless cards
    Requires hostapd, dnsmasq
    """
    def __init__(self):
        self.interface = 'wlan0'
        self.dhcp = ManageDHCP()

    # def run(self):
    #     while self.svc.apmode is True:
    #         self.startap()
    #     self.stopap()

    def startap(self):
        logging.info("Starting WiFi AP")
        self.dhcp.start()
        try:
            os.system('sudo ifconfig {} down'.format(self.interface))
            os.system('sudo rfkill unblock {}'.format(self.interface))  # Remove possible WLAN block
            os.system('sudo ifconfig {} 10.15.0.1/24 up'.format(self.interface))
        except Exception as e:
            logging.warning('Unable to prepare WiFi AP interface: {}'.format(e))
        try:
            os.system('sudo service hostapd start')
            self.svc.ap_active = True
        except Exception as e:
            logging.critical("Unable to start WiFi AP: {}".format(e))
            self.svc.ap_active = False

    def stopap(self):
        logging.info("Stopping WiFi AP")
        self.dhcp.stop()
        try:
            os.system('sudo service hostapd stop')
        except Exception as e:
            logging.critical("Unable to stop WiFi AP: {}".format(e))
        finally:
            os.system('sudo ifconfig {} down'.format(self.interface))
            os.system('sudo ifconfig {} up'.format(self.interface))
            self.svc.ap_active = False
