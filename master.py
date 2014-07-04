import os
import sys
import time
import socket
import logging
from datetime import datetime

import pytz

from apscheduler.scheduler import Scheduler
import graypy  # for logging to graylog
import common  # our common files used in projects


class Master(object):
    '''Primary Application Daemon Object'''
    def __init__(self, cfg=None):
        '''Initialize the Application Master Object'''
        self.hostname = socket.gethostname()
        self.cfg = None
        self.env = None
        self.set_cfg(cfg)
        self.set_env()
        self._shutdown = False
        self.collectors = {}
        self._workers = []
        self.ready = False
        socket.setdefaulttimeout(15)
        self.sched = Scheduler()
        self.setup_logging()
        #self.metrics = common.Metrics(namespace='$$.{}.$$.{}'.format(self.env, self.hostname))
        #self.setup_default_metrics()
        self.jobs = common.Jobs(self)
        self._status = {'status': 'init',
                        'hostname': self.hostname,
                        'environment': self.env,
                        'threadstatus': {},
                        }
        self.setloglvl(self.cfg.logging['loglevel'])
        logging.info("Init Complete")

    def set_cfg(self, cfg=None):
        '''Set the configuration based on passed in value or default to _cfg_filepath()

        :param cfg: Override default configuration
        :type cfg: dict
        '''
        if cfg is not None:
            self.cfg = cfg
        else:
            self.cfg = common.Settings(self._cfg_filepath())
        return cfg  # for testing

    def _cfg_filepath(self):
        '''Searches for a configuration file and returns its path'''
        paths = []
        paths.append(os.path.dirname(os.path.abspath(__file__)))
        paths.append('..')
        paths.append('./common')  # enter path to append
        for fp in paths:
            f = os.path.join(fp, 'config_file.cfg')
            if os.path.exists(f):
                return f
        logging.critical("No Config Found")
        raise Exception("No Config Found")

    @property
    def shutdown(self):
        '''Shutdown property, when true, threads will start exiting.'''
        return self._shutdown

    @shutdown.setter
    def shutdown(self, please):
        '''
        Sets the shutdown attribute, call with please=True to initiate shutdown.

        :param please: Override default configuration
        :type please: bool
        '''
        if please is True:
            self._shutdown = True
            logging.info("Initiating Shutdown")
        return self._shutdown

    def start(self):
        '''Start everything'''
        logging.info("Startup")
        self.start_ws()
        self.schedule_tasks()
        self._status['status'] = 'running'
        self.main_loop()

    def initial_tasks(self):
        '''Runs a few jobs immediately upon startup'''
        pass

    def schedule_tasks(self):
        '''Schedule routine tasks'''
        #self.sched.add_interval_job(self.jobs.a_job(), minutes=self.splay_tasks(1))
        #self.sched.start()

    def splay_tasks(self, n):
        if self.env == 'production':
            return n
        else:
            return int(n + n)

    def setup_logging(self):
        '''Setup Logging, assuming we're logging to graylog using graypy'''
        if self.env == "production":
            facilityname = "ApplicationName"
        else:
            facilityname = "Application-Dev"

        log = logging.getLogger(facilityname)
        logformat = logging.Formatter(fmt='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        log.setLevel('INFO')
        if self.cfg.graypy['enable']:
            handler = graypy.GELFHandler(self.cfg.graypy['host'], int(self.cfg.graypy['port']))
            handler.setFormatter(logformat)
            log.addHandler(handler)
        else:
            handler = logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
            logging.StreamHandler(sys.stdout)
            log.addHandler(handler)
        logging.info("Initializing Application")

    def setloglvl(self, loglevel):
        '''Is called to set the log level'''
        logging.info("Setting Log Level: {0}".format(loglevel))
        if loglevel == 'INFO':
            logging.root.setLevel(logging.INFO)
        elif loglevel == 'WARN':
            logging.root.setLevel(logging.WARN)
        elif loglevel == 'DEBUG':
            logging.root.setLevel(logging.DEBUG)

    def set_env(self, override=None):
        '''Set Environment'''
        if override is not None:
            self.env = override
        elif 'sysctl' in self.hostname:
            self.env = 'production'
        else:
            self.env = 'dev'
        return self.env  # for testing

    def status(self):
        """Make a copy of status dict and return it"""
        currentstatus = self._status.copy()
        return currentstatus

    def start_ws(self):
        """Start the web service"""
        ws = common.WS(self)
        ws.setDaemon(True)
        ws.start()

    def set_threadstatus(self, thread, status):
        if not thread in self._status['threadstatus'].keys():
            self._status['threadstatus'][thread] = {}
        self._status['threadstatus'][thread]['ts'] = datetime.now(pytz.timezone('US/Mountain'))
        self._status['threadstatus'][thread]['status'] = str(status)
        logging.debug("Status: {1}".format(thread, status))

    def cleanup(self):
        logging.info("Entering Cleanup")

    def main_loop(self):
        self.ready = True
        try:
            logging.info("Main Thread Stable (startup complete)")
            self.initial_tasks()
            while self.shutdown is not True:
                try:
                    time.sleep(15)
                    self.set_threadstatus("MAIN", "LOOP")
                    ## do stuff
                except KeyboardInterrupt:
                    self.keyboardinterrupt()
            self.set_threadstatus("MAIN", "CLEANUP")
            self._status['status'] = 'cleanup'
            logging.info("Begin Shutdown Sequeuence")
            self.cleanup()
            logging.info("System Database Shutdown")
        except Exception as e:
            logging.critical("Error in Main loop: {0}".format(e))
        finally:
            exit()

    def keyboardinterrupt(self):
        self.shutdown = True
        logging.info("KeyboardInterrupt Called, Shutting down application")
