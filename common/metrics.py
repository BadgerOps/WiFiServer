from threading import Lock
import time


class Metrics(object):
    def __init__(self, namespace=''):
        self.ns = namespace
        self._metrics = {}
        self._dump_lock = Lock

    def add_counter(self, name):
        if name not in self._metrics:
            self._metrics[name] = Counter(name)

    def increment_counter(self, name, step=1):
        if name not in self._metrics:
            self._metrics[name] = Counter(name)
        self._metrics[name].increment(step=1)

    def graphite_get_reset(self, locking=True):
        '''wraps _grafitegetreset with optional locking (enabled by default)'''
        if locking is True:
            with self._dump_lock():
                return self._graphitegetreset()
        else:
            return self._graphitegetreset()

    def update_static(self, name, value, temporary=False):
        if name not in self._metrics:
            self._metrics[name] = Static(name, value, temporary)
        else:
            self._metrics[name].update(value)

    def _graphitegetreset(self):
        temp = []
        for name, metric in self._metrics.iteritems():
            temp.append("{}.{} {} {}".format(self.ns, name, metric.dump(), int(time.time())))
            try:
                if metric.temporary is True:
                    del self._metrics['name']
            except Exception:
                pass
        return temp



class Static(object):
    def __init__(self, name, value, temporary=False, reset=True, default=0):
        self.temporary = temporary
        self.value = value
        self.name = name
        self.reset = reset
        self.default = default

    def update(self, value):
        self.value

    def dump(self):
        t = self.value
        if self.reset is True:
            self.value = self.default
        return t


class Counter(object):
    def __init__(self, name):
        self.temporary = False
        self.value = 0
        self.name = name

    def increment(self, step):
        self.value += step

    def dump(self):
        temp = self.value
        self.value = 0
        return temp



