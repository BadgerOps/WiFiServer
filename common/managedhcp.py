import logging
import os
import sys


class ManageDHCP(object):
    def __init__(self):
        pass

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
