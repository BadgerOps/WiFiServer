#!/usr/bin/env python

# pylint: disable=W0611,W0612,R0912


import threading
import logging
from bottle import route, run, get, post, request, response, error, HTTPError
import json


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

        @get('/scan')
        def scan():
            self.wifiserver.get_networks()
            return self.wifiserver.networks

        @post('/add_network')
        def add_network():
            data = request.json
            response.content_type = 'application/json'
            result = self.wifiserver.add_network(data)
            return json.dumps(result)

        @get('/shutdown/please')
        def shutdown():
            self.wifiserver.shutdown = True
            return "Shutting Down"

        while True:
            try:
                run(host='0.0.0.0', port=8080, quiet=True) #  TODO: set port in config
            except Exception:
                logging.critical("exception in webservice", exc_info=1)
