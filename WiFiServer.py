#!/usr/bin/env python

import logging
import sys
import time
from datetime import datetime
import common

class WiFiServer(object):

    def __init__(self, cfg=None):
        self.setup_logging()
        self.shutdown = False
        self.networks = []


    def setup_logging(self):
        """Setup Logging"""
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.StreamHandler(sys.stdout)

    def keyboardinterrupt(self):
        self.shutdown = True
        logging.info("KeyboardInterrupt Called, Shutting down application")

    def start(self):
        self.main()

    def get_networks(self):
        wificlient = common.WifiClient
        self.networks = wificlient.scan

    def main(self):
        """main thread"""
        try:
            logging.info("Main Thread Stable (startup complete)")
            while self.shutdown == False:
                try:
                    time.sleep(15)
                    logging.debug('in the main loop')
                    print 'performing network scan'
                    self.get_networks()
                    print self.networks
                    #self.set_threadstatus("MAIN", "LOOP")
                    ## do stuff
                except KeyboardInterrupt:
                    self.keyboardinterrupt()
            # self.set_threadstatus("MAIN", "CLEANUP")
            # self._status['status'] = 'cleanup'
            logging.info("Begin Shutdown Sequeuence")
            #self.cleanup()
            logging.info("WiFiServer is Shutdown")
        except Exception as e:
            logging.critical("Error in Main loop: {0}".format(e))
        finally:
            exit()