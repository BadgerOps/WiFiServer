#!/usr/bin/env python

import os
import logging
import threading
from time import sleep
from common.svc import WiFiObj, MyConfigParser
from managedhcp import ManageDHCP


class WiFiAP(threading.Thread):
    """
    Allows creation and management of WiFi AP on compatible wireless cards
    Requires hostapd, dnsmasq
    """
    def __init__(self, wifiserver):
        self.interface = None
        self.wifiserver = wifiserver
        self.get_cfg()
        self.dhcp = ManageDHCP()
        threading.Thread.__init__(self)

    def run(self):
        while not self.wifiserver.shutdown:
            if self.wifiserver.svc.apmode:
                if not self.wifiserver.svc.ap_active:
                    self.startap()
            else:
                if self.wifiserver.svc.ap_active:
                    self.stopap()

    def startap(self):
        logging.info("Starting WiFi AP")
        self.dhcp.start()
        try:
            os.system('sudo ifconfig {} down'.format(self.interface))
            os.system('sudo killall wpa_supplicant')
            os.system('sudo ifconfig {} 10.0.0.1/24 up'.format(self.interface))
            sleep(5)
            logging.debug("Successfully prepared interface")
        except Exception as e:
            logging.warning('Unable to prepare WiFi AP interface: {}'.format(e))
        try:
            os.system('sudo service hostapd start')
            sleep(5)
            logging.info("WiFi AP Stable")
            self.wifiserver.svc.ap_active = True
        except Exception as e:
            logging.critical("Unable to start WiFi AP: {}".format(e))
            self.wifiserver.svc.ap_active = False

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
            self.wifiserver.svc.ap_active = False

    def get_cfg(self):
        cfg = MyConfigParser()
        cfg.read("/etc/hostapd/hostapd.conf")
        self.interface = cfg.get("hostapd", "interface")
