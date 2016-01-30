import os
import ConfigParser
from ConfigParser import InterpolationMissingOptionError

# Environment variable defining dockeri base dir: 'DOCKERIRDIR'
# Inside this dir should be the dirs/files:
# -/conf.d
# -/bin

class Config:
    main     = { 'image'  : '' }
    volumes  = { 'input'  : 'input',
                 'output' : 'output',
    }
    ports    = {}

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

        # verify the 'ports' section
        if not d.has_key('ports'):
            d['ports'] = {}
        _d = self.ports.copy()
        _d.update(d['ports'])
        d['ports'].update(_d)

        # verify the 'volumes' section
#        if not d.has_key('volumes'):
#            d['volumes'] = {}
#        dsec = d['volumes']
#        for k,v in self.volumes.items():
#            if not dsec.has_key(k):
#                dsec[k] = v
        if not d.has_key('volumes'):
            d['volumes'] = {}
        _d = self.volumes.copy()
        _d.update(d['volumes'])
        d['volumes'].update(_d)

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

def select_file(fileslist,image):
    for f in fileslist:
        root = os.path.basename(f).split('.')[0]
        if root == image:
            return f
    return None

def read_dir(configdir):
    from glob import glob
    import os
    _abspath = os.path.abspath(configdir)
    cfiles = glob(os.path.join(_abspath,'*.cfg'))
    return cfiles

def config_files(DOCKERIR_DIR=None):
    import os
    DOCKERIRDIR = ""
    if os.environ.has_key('DOCKERIRDIR'):
        DOCKERIRDIR = os.environ['DOCKERIRDIR']
    if DOCKERIR_DIR:
        DOCKERIRDIR = DOCKERIR_DIR
    cfiles = read_dir(os.path.join(DOCKERIRDIR,'conf.d'))
    return cfiles

def main(image,DOCKERDIR=None):
    cfiles = config_files(DOCKERDIR)
    cfgfile = select_file(cfiles,image)
    cfg = parse_file(cfgfile)
    return cfg
