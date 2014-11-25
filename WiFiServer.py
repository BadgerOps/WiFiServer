#!/usr/bin/env python


import sys
import time
from apscheduler.scheduler import Scheduler
import logging
import common


class WiFiServer(object):
    """
    Main thread for WiFi service
    """
    def __init__(self):
        self.rpi = False  # TODO: do this programmatically
        self.debugging = True  # TODO: remove this before packaging
        self.svc = common.SVC()
        common.WiFiObj.svc = self.svc
        self.ap = None
        self.ws = None
        self.setup_logging()
        self.shutdown = False
        self.networks = []

    def setup_logging(self):
        """Setup Logging"""
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        if self.debugging:  # read this from config / init
            logging.StreamHandler(sys.stdout)
        else:
            handler = logging.FileHandler('/var/log/wifiserver.log')
            logging.addHandler(handler)
            
    def setup_scheduler(self):
        """setup periodic jobs"""
        sched = Scheduler()
        sched.start()
        sched.add_interval_job(self.get_networks, seconds=5)

    def get_networks(self):  # TODO: depricate
        """get a list of networks, being depricated"""
        wificlient = common.WifiClient(self)
        self.networks = wificlient.scan()
        logging.debug(self.networks.keys())

    def add_network(self, data):
        """add new network config information"""
        wificlient = common.WifiClient(self)
        result = wificlient.add_network(data)
        return result
    
    def list_network(self):
        """for the ws endpoint, send a list of the network ssids"""
        return self.networks.keys()
    
    def join_network():
        """on startup, try to join a saved network"""
        pass
    
    def cleanup(self):
        """on shutdown, we may need to clean some stuff up"""
        logging.info("Cleaning Up")
        self.ap.stopap()
        self.ap.join(timeout=10)
        self.ws.join(timeout=10)

    def start_ap(self):
        """
        Start up AP
        :return: None
        """
        self.ap = common.WiFiAP(self)
        self.ap.setDaemon(True)
        self.ap.start()

    def start_ws(self):
        """Start the web service"""
        self.ws = common.WS(self)
        self.ws.setDaemon(True)
        self.ws.start()

    def keyboardinterrupt(self):
        self.shutdown = True

        logging.info("KeyboardInterrupt called, cleaning up and shutting down application")

    def start(self):
        """called from the run.py file, this starts each thread, then the main"""       
        self.setup_scheduler()
        if self.rpi:
            self.check_jumper()
        self.start_ws()
        if self.svc.apmode:
            self.start_ap()
        elif self.svc.client_mode:
            self.join_network()
        else:
            pass
        self.main()
        
    def check_jumper(self):
        """if we're on a raspberry pi, we check to see if the
        jumper is on or off, AP mode or Client mode"""
        if common.RpiHW.gpio_check:
            self.svc.client_mode = False
            self.svc.apmode = True
        elif not common.RpiHW.gpio_check:
            self.svc.apmode = False
            self.svc.client_mode = True
            
    def check_mode(self):
        """check which mode we're in, set up / tear down accordingly"""
        pass
    
    def main(self):
        """main thread"""
        try:
            logging.info("Main Thread Stable (startup complete)")
            while self.shutdown is False:
                try:
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    self.keyboardinterrupt()
            logging.info("Begin Shutdown Sequence")
            self.cleanup()
            logging.info("WiFiServer is Shutdown")
        except Exception as e:
            logging.critical("Error in Main loop: {0}".format(e))
        finally:
            exit()
