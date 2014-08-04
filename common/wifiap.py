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
        while self.svc.apmode is True:
            self.startap()
        self.stopap()

    def startap(self):
        logging.info("Starting WiFi AP")
        try:
            something
        except Exception as e:
            logging.warn("exceptiony stuff")

    def stopap(self):
        logging.info("Stopping WiFi AP")
        try:
            something
        except Exception as e:
            logging.warn("agh!")
