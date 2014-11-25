#!/usr/bin/env python

# pylint: disable=W0611,W0612,R0912


import threading
import logging
from bottle import route, run, get, post, request, response, error, HTTPError, static_file
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
            return static_file('index.html', 'common/static')

        @route('/bootstrap.css')
        def css():
            return static_file('bootstrap.min.css', 'common/static')

        @route('/jquery.js')
        def js():
            return static_file('jquery-1.11.1.min.js', 'common/static')

        @route('/status')
        def status():
            response.contenttype = 'application/json'
            return {
                'apmode': self.wifiserver.svc.apmode,
                'connected_ssid': self.wifiserver.svc.connected_ssid,
                }

        @get('/list')
        def list():
            response.content_type = 'application/json'
            return json.dumps(self.wifiserver.list_network())            

        @get('/scan')
        def scan():
            self.wifiserver.get_networks()
            return self.wifiserver.networks

        @route('/add_network', method='POST')
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
