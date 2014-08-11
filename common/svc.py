import logging
import ConfigParser
import StringIO


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
        self.ap_active = False
        self.client_mode = False


class MyConfigParser(ConfigParser.ConfigParser):
    """
    Subclassed Configparser and overrode the read method, since Hostapd doesn't like INI sections...
    """
    def read(self, filename):
        try:
            with open(filename) as cfgfile:
                text = cfgfile.read()
        except IOError:
            pass
        else:
            file = StringIO.StringIO("[hostapd]\n" + text)
            self.readfp(file, filename)
