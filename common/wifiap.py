#!/usr/bin/env python

import logging
import os
import sys
import configparser
from svc import WiFiObj
from time import sleep
from managedhcp import ManageDHCP


class WiFiAP(WiFiObj):
    """
    Allows creation and management of WiFi AP on compatible wireless cards
    Requires hostapd, dnsmasq, network-manager
    """
    def __init__(self):
        self.dhcp = ManageDHCP()

    def run(self):
        while self.svc.apmode:
            logging.info("Starting WiFi AP")
            try:
                self.startap()
            except Exception as e:
                logging.critical("Unable to start WiFi AP: {}".format(e))
        logging.info("Shutting down WiFi AP")
        try:
            self.stopap()
        except Exception as e:
            logging.warn("Unable to stop WiFi AP: {}".format(e))

    def startap(self):
        pass

    def stopap(self):
        pass

