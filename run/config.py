import os
import ConfigParser
from ConfigParser import InterpolationMissingOptionError

class Config:
    main     = { 'image'  : None }
    volumes  = { 'input'  : 'input',
                 'output' : 'output',
    }

    def __init__(self,configfile,defaults={}):
        self.parser = self.parse(configfile,defaults)
        self.config = self.filter()

    def parse(self,configfile,defaults):
        parser = ConfigParser.SafeConfigParser(defaults,allow_no_value=True)
        parser.read(configfile)
        return parser

    def filter(self):
        d = {}
        parser = self.parser
        for sec in parser.sections():
            dsec = {}
            try:
                for k,v in parser.items(sec):
                    dsec[k] = v
            except InterpolationMissingOptionError,e:
                print e
            d[sec] = dsec
        # verify the 'volumes' section
        if not d.has_key('volumes'):
            d['volumes'] = {}
        dsec = d['volumes']
        for k,v in self.volumes.items():
            if not dsec.has_key(k):
                dsec[k] = v
        # verify the 'main' section
        if not d.has_key('main'):
            d['main'] = {}
        _d = self.main.copy()
        _d.update(d['main'])
        d['main'].update(_d)
        return d

    def configs(self):
        return self.config

def parse_file(configfile,defaults={}):
    #filename = os.path.basename(configfile)
    #_alias = filename.split('.')[0]
    config = Config(configfile,defaults)
    return config.configs()


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    d = parse_file(filename)
    for k,v in d.items():
        print k,v

