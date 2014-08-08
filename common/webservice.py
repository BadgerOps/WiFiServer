#!/usr/bin/env python

# pylint: disable=W0611,W0612,R0912


import threading
import logging
from bottle import route, run, get
from common import jsondump, json_handler


class WS(threading.Thread):
    """simple bottle web service for our API endpoints"""

    def __init__(self, wifiserver):
        self.wifiserver = wifiserver
        threading.Thread.__init__(self)

    def run(self):
        """run the webservice"""
        while self.wifiserver.shutdown is False:
            logging.info("starting the webservice")
            self.server()

    def server(self):
        """main webserver object"""
        @route('/')
        def index():
            return "Index should go here, readme?"

        @get('/list')
        def list():
            return self.wifiserver.networks

    while True:
        try:
            run(host='0.0.0.0', port=8080, quiet=True)
        except Exception:
            logging.critical("exception in webservice", exc_info=1)
