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
        self.update_cfg

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

    def update_cfg(self):
        apcfg = """interface=wlan0
                driver=nl80211
                ssid=wifi_server
                hw_mode=g
                channel=6
                macaddr_acl=0
                auth_algs=1
                ignore_broadcast_ssid=0
                wpa=3
                wpa_passphrase=wifi_server
                wpa_key_mgmt=WPA-PSK
                wpa_pairwise=TKIP
                rsn_pairwise=CCMP"""
        with file('/etc/hostapd.conf', mode='w+') as cfg:
            cfg.write(apcfg)