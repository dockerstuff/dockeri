import os
import configparser
from configparser import InterpolationMissingOptionError
from glob import glob
import shutil

# Environment variable defining dockeri base dir: 'DOCKERIRDIR'
# Inside this dir should be the dirs/files:
# -/conf.d
# -/bin

DOCKERI_DEFAULT_DIR='$HOME/.dockeri'
HERE=os.path.abspath(os.path.dirname(__file__))

class Config:
    main     = {'image' : ''}
    volumes  = {'io'    : 'io'}
    ports    = {}

    def __init__(self, configfile=None, defaults={}):
        self.parser = None
        if configfile:
            self.parser = self.parse(configfile, defaults)
        self.config = self.filter()

    def parse(self, configfile, defaults):
        parser = configparser.SafeConfigParser(defaults, allow_no_value=True)
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
            except InterpolationMissingOptionError as e:
                print(e)
            d[sec] = dsec
        return d

    def filter(self):
        d = self._parser2dict()

        # verify the 'ports' section
        if 'ports' not in d:
            d['ports'] = {}
        _d = self.ports.copy()
        _d.update(d['ports'])
        d['ports'].update(_d)

        # verify the 'volumes' section
        if 'volumes' not in d:
            d['volumes'] = {}
        _d = self.volumes.copy()
        _d.update(d['volumes'])
        d['volumes'].update(_d)

        # verify the 'main' section
        if 'main' not in d:
            d['main'] = {}
        _d = self.main.copy()
        _d.update(d['main'])
        d['main'].update(_d)

        return d

    def configs(self):
        return self.config


def parse_file(configfile, defaults={}):
    config = Config(configfile, defaults)
    return config.configs()


def select_file(fileslist, image):
    for f in fileslist:
        root = os.path.basename(f).split('.')[0]
        if root == image:
            return f
    return None


def read_dir(configdir):
    _abspath = os.path.abspath(configdir)
    cfiles = []
    if os.path.isdir(_abspath):
        cfiles = glob(os.path.join(_abspath, '*.cfg'))
    return cfiles


def config_files(DOCKERI_DIR=None):
    DOCKERIUSER = ""
    # if 'DOCKERIUSER' in os.environ:
    #     DOCKERIUSER = os.environ['DOCKERIUSER']
    if DOCKERI_DIR:
        DOCKERIUSER = DOCKERI_DIR
    else:
        DOCKERIUSER = os.path.expandvars(DOCKERI_DEFAULT_DIR)
        if not os.path.isdir(DOCKERIUSER):
            os.mkdir(DOCKERIUSER)
        DOCKERICONF = os.path.join(DOCKERIUSER, 'conf.d')
        if not os.path.isdir(DOCKERICONF):
            os.mkdir(DOCKERICONF)
            for fcfg in glob(os.path.join(HERE, 'conf.d', '*.cfg')):
                shutil.copy(fcfg, DOCKERICONF)
    cfiles = read_dir(DOCKERICONF)
    return cfiles


def main(image, DOCKERDIR=None):
    cfiles = config_files(DOCKERDIR)
    cfgfile = select_file(cfiles, image)
    cfg = parse_file(cfgfile)
    return cfg
