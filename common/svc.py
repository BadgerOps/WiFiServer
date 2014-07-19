import logging
from wifiap import WiFiAP


class WiFiObj(object):
    """
    Common object to inherit from, provides access to services/information
    """
    svc = None


class SVC(object):
    """
    Used by WiFiObj to actually provide services/information to child objects
    """
    def __init__(self):
        self.cfg = None
        self.apmode = True
        self.ap = WiFiAP()