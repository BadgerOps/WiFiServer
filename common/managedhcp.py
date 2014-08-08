import logging
import os


class ManageDHCP(object):
    """
    Pretty simple object to handle starting/stopping DHCP
    May eventually handle config
    """
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
