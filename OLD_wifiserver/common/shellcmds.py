import logging
import os
import subprocess
import time
try:
    from signal import SIGKILL
except ImportError:
    #For windows compatibility
    from signal import SIGTERM as SIGKILL

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.stdout = None
        self.stderr = None
        self.status = None
        self.runtime = None
        self.timeout = None
        self.timeoutreached = False

def run(cmd=None, timeout=None):
    '''expects command to run and optionally a timeout (in seconds)
    returns output, stderr, status and runtime'''
    cmdresult = Command(cmd)

    start_time = time.time()

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not timeout:
        cmdresult.status = p.wait()
    else:
        timeout_time = start_time + timeout
        while p.poll() is None and timeout_time > time.time():
            time.sleep(.25)
            if timeout_time < time.time():
                os.kill(p.pid, SIGKILL)
                cmdresult.runtime = round(time.time() - start_time, 2)
                cmdresult.timeoutreached = True

    cmdresult.status = p.returncode
    cmdresult.stdout, cmdresult.stderr = p.communicate()
    cmdresult.runtime = round(time.time() - start_time, 2)
    return cmdresult
