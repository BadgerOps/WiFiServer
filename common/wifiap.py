#!/usr/bin/env python

import logging
import os
import sys
import configparser
from time import sleep
from managedhcp import ManageDHCP


class WiFiAP(wifiobj):
    """
    Allows creation and management of WiFi AP on compatible wireless cards
    Requires hostapd, dnsmasq, network-manager
    """
    def __init__(self):
        self.dhcp = ManageDHCP()

    def run(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

