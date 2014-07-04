#!/usr/bin/env python

# pylint: disable=W0611,W0612,R0912


from time import sleep
import threading
import logging

from bottle import route, run, get

from common import jsondump


class WS(threading.Thread):
    def __init__(self, main):
        self.main = main
        threading.Thread.__init__(self)

    def run(self):
        self.setName("WEBSVC")
        while self.main.shutdown is False:
            sleep(1)
            logging.info("Starting Webservice")
            self.server()

    def server(self):
        @route('/')
        def index():
            return "generic application - WS"

        @route('/nagios')
        def nagios():
            status = {"status_code": 0, "status_msg": "OK (static)"}  # fixme
            return jsondump(status)

        @get('/status')
        def status():
            return jsondump(self.main._status)

        @get('/shutdown/now')
        def shutdownnow():
            logging.info("Shutdown Called from WS")
            self.main.shutdown = True

        while True:
            try:
                run(host='0.0.0.0', port=int(self.main.cfg.ws['port']), quiet=True)
            except Exception as e:
                sleep(2)
                logging.critical(e, exc_info=1)
