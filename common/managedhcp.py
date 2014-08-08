import logging
import os


class ManageDHCP(object):
    def __init__(self):
        self.update_cfg()

    def start(self):
        try:
            os.system('sudo service dnsmasq start')
        except Exception as e:
            logging.warning('Unable to start dnsmasq: {}'.format(e))

    def stop(self):
        try:
            os.system('sudo service dnsmasq stop')
        except Exception as e:
            logging.warning('Unable to stop dnsmasq: {}'.format(e))

    def update_cfg(self):
        dnscfg = """
                no-resolv
                interface=wlan0
                dhcp-range=10.0.0.3,10.0.0.20,12h"""
        with file('/etc/dnsmasq.conf', mode='w+') as cfg:
            cfg.write(dnscfg)