#!/usr/bin/env python

import logging
import sys
import time
import common


class WiFiServer(object):
    """
    Master process for WiFi service
    """
    def __init__(self, cfg=None):
        self.svc = common.SVC()
        common.WiFiObj.svc = self.svc
        self.ap = common.WiFiAP(self)
        self.setup_logging()
        self.shutdown = False
        self.networks = []

    def setup_logging(self):
        """Setup Logging"""
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        logging.StreamHandler(sys.stdout)

    def get_networks(self):
        wificlient = common.WifiClient()
        self.networks = wificlient.scan()

    def add_network(self, data):
        """add new network config information"""
        wificlient = common.WifiClient()
        result = wificlient.add_network(data)
        return result

    def cleanup(self):
        """on shutdown, we may need to clean some stuff up"""
        self.ap.stopap()

    def start_ws(self):
        """Start the web service"""
        ws = common.WS(self)
        ws.setDaemon(True)
        ws.start()

    def keyboardinterrupt(self):
        self.shutdown = True
        self.cleanup()
        logging.info("KeyboardInterrupt called, cleaning up and shutting down application")

    def start(self):
        """called from the run.py file, this starts each thread, then the main"""
        self.start_ws()
        self.ap.run()
        self.main()

    def main(self):
        """main thread"""
        try:
            logging.info("Main Thread Stable (startup complete)")
            while self.shutdown is False:
                try:
                    time.sleep(1)
                    logging.debug('Main loop')
                except KeyboardInterrupt:
                    self.keyboardinterrupt()
            logging.info("Begin Shutdown Sequeuence")
            self.cleanup()
            logging.info("WiFiServer is Shutdown")
        except Exception as e:
            logging.critical("Error in Main loop: {0}".format(e))
        finally:
            exit()
