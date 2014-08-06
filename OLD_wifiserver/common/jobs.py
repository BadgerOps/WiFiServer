import logging

from common import jsondump


class Jobs(object):
    '''example of a jobs class'''
    def __init__(self, main):
        self.main = main

    def a_job(self):
        '''example of a job including a json conversion tool'''
        info = ['list, of, info']
        information = jsondump(info)
        logging.info('info was converted to json-friendly format')
        pass