import re
from datetime import datetime

class LogDicts:

    def __init__(self, filename):
        self._log_lines = self._load_file(filename)
        self.earliest_dict = None
        self.latest_dict = None

    def _load_file(self, filename):
        with open(filename) as f:
            return f.readlines()

    def _line_to_dict(self, line):
        pattern = r'''
        # IP addresses contain four numbers (each with 1-3 digits)
            (?P<ip_address>(?:\d{1,3}\.){3}\d{1,3}) 
        # Junk between IP address and timestamp
            .*
        # Timestamp, defined to be anything between [ and ]
            \[(?P<timestamp>[^\]]+)\]
        # Junk between timestamp and request
            .*
        # Request, starting with GET
            "(?P<request>GET[^"]+)"                 
        '''
        match = re.search(pattern, line, re.X)
        if match:
            output = match.groupdict()
        else:
            output = {'ip_address': 'No IP address found',
                      'timestamp': 'No timestamp found',
                      'request': 'No request found'}
        return output

    def _sorting_choice(self, obj, key):
        if key:
            return (item for item in sorted(obj, key=key))
        else:
            return obj
    
    def iterdicts(self, key=None):
        out = (self._line_to_dict(line) for line in self._log_lines)
        return self._sorting_choice(out, key)

    def dicts(self, key=None):
        out = [self._line_to_dict(line) for line in self._log_lines]
        if key:
            return sorted(out, key=key)
        else:
            return out

    def _time_convert(self, entry):
        return datetime.strptime(entry['timestamp'], '%d/%b/%Y:%H:%M:%S %z')   

    def latest(self):
        if self.latest_dict is None:
            idx = max((self._time_convert(entry), idx)
                      for idx, entry in enumerate(self.iterdicts()))[1]
            self.latest_dict = [self._line_to_dict(line) 
                                for line in self._log_lines][idx]
        return self.latest_dict

    def earliest(self):
        if self.earliest_dict is None:
            idx = min((self._time_convert(entry), idx)
                      for idx, entry in enumerate(self.iterdicts()))[1]
            self.earliest_dict = [self._line_to_dict(line) 
                                for line in self._log_lines][idx]
        return self.earliest_dict

    def for_ip(self, ip_address, key=None):
        out = (self._line_to_dict(line) for line in self._log_lines 
               if self._line_to_dict(line)['ip_address'] == ip_address)
        return self._sorting_choice(out, key)

    def for_request(self, text, key=None):
        out = (self._line_to_dict(line) for line in self._log_lines 
               if text in self._line_to_dict(line)['request'])
        return self._sorting_choice(out, key)





