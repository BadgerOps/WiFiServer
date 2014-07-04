from datetime import datetime, timedelta
import json


def jsonhandler(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, timedelta):
        return int(obj.total_seconds())
    elif isinstance(obj, set):
        return list(obj)
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif hasattr(obj, 'json'):
        return obj.json()
    else:
        raise TypeError('Object of type {0} with value of {1} is not JSON serializable'.format(type(obj), repr(obj)))


def jsondump(raw):
    return json.dumps(raw, default=jsonhandler)
