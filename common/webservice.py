#!/usr/bin/env python

# pylint: disable=W0611,W0612,R0912


import threading
import logging
from bottle import route, run, get, post, request, response, error, HTTPError
import json



# the decorator to enable Cross Origin Resource Sharing
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


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

        @route('/scan', method=['OPTIONS','GET'])
        @enable_cors
        def scan():
            logging.info("got a /scan request")
            self.wifiserver.get_networks()
            logging.info("returning from /scan")
            return self.wifiserver.networks

        @route('/add_network', method=['OPTIONS','POST'])
        @enable_cors
        def add_network():
            data = request.json
            logging.info("got an /add_network request")
            logging.info(request)
            logging.info("method")
            logging.info(request.method)
            logging.info("content type = ")
            logging.info(request.content_type)
            logging.info("json")
            logging.info(request.json)
            logging.info("name")
            logging.info(request.json['name'])
            logging.info("passkey")
            logging.info(request.json['passkey'])
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
