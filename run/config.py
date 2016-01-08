import os
import ConfigParser
from ConfigParser import InterpolationMissingOptionError

# Environment variable defining dockeri base dir: 'DOCKERIRDIR'
# Inside this dir should be the dirs/files:
# -/conf.d
# -/src
# -/bin

class Config:
    main     = { 'image'  : '' }
    volumes  = { 'input'  : 'input',
                 'output' : 'output',
    }

    def __init__(self,configfile=None,defaults={}):
        self.parser = None
        if configfile:
            self.parser = self.parse(configfile,defaults)
        self.config = self.filter()

    def parse(self,configfile,defaults):
        parser = ConfigParser.SafeConfigParser(defaults,allow_no_value=True)
        parser.read(configfile)
        return parser

    def _parser2dict(self):
        d = {}
        parser = self.parser
        if not parser:
            return d
        for sec in parser.sections():
            dsec = {}
            try:
                for k,v in parser.items(sec):
                    dsec[k] = v
            except InterpolationMissingOptionError,e:
                print e
            d[sec] = dsec
        return d

    def filter(self):
        d = self._parser2dict()
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

def read_dir(configdir,image):
    from glob import glob
    import os
    _abspath = os.path.abspath(configdir)
    cfiles = glob(os.path.join(_abspath,'*.cfg'))
    def select_file(fileslist,image):
        for f in fileslist:
            root = os.path.basename(f).split('.')[0]
            if root == image:
                return f
        return None
    imagecfg = select_file(cfiles,image)
    return imagecfg

def main(image,DOCKERIR_DIR=None):
    import os
    DOCKERIRDIR = ""
    if os.environ.has_key('DOCKERIRDIR'):
        DOCKERIRDIR = os.environ['DOCKERIRDIR']
    if DOCKERIR_DIR:
        DOCKERIRDIR = DOCKERIR_DIR
    cfgfile = read_dir(os.path.join(DOCKERIRDIR,'conf.d'),image)
    cfg = parse_file(cfgfile)
    return cfg
