#!/usr/bin/env python

import argparse
import os

def available_configs():
    import config
    cfgfiles = config.config_files()
    imagesAvail = [ os.path.basename(fn).split('.')[0] for fn in cfgfiles ]
    return imagesAvail

parser = argparse.ArgumentParser(description='Interface for Docker containers.')

parser.add_argument('image', choices=available_configs(),
        help='alias/name of the image to run.')

parser.add_argument('-w','--io',dest='io_dir',default=None,
        help='host directory to use for files I/O with container')

# parser.add_argument('-o','--output',dest='output_dir',default=None,
#         help='host directory to use as output for the container')

parser.add_argument('-f','--file',dest='filename',
        help='filename (found inside io-dir) to argument the container entrypoint')

parser.add_argument('-x',dest='with_x11',action='store_true',
        help='route x11 from the container?')

args = parser.parse_args()

cmdline = 'docker run -it'

# read the default config for system/image
import config
cfg = config.main(args.image)

# image name at Hub
i_cfg = cfg['main'].get('image')
image = i_cfg if i_cfg is not '' else args.image

# i/o volumes
## HACK
for d,h in cfg['volumes'].items():
    if d != 'io':
        _ddir = os.path.abspath(os.path.expandvars(d))
        _hdir = os.path.abspath(os.path.expandvars(h))
        cmdline += ' -v {0}:{1}'.format(_hdir,_ddir)
iodir_cfg = cfg['volumes']['io'] if args.io_dir is None else args.io_dir
iodir_cfg = os.path.abspath(iodir_cfg)
cmdline += ' -v {0}:{1}'.format(iodir_cfg,'/work/io')

# option for accessing the x11
if args.with_x11:
    import x11
    _x11 = '/tmp/.X11-unix'
    _dsp = x11.get_DISPLAY()
    cmdline += ' -v {0}:{1} -e DISPLAY={2}'.format(_x11,_x11,_dsp)

# option for port mappings
if len(cfg['ports'].keys()) > 0:
    for p_cont,p_host in cfg['ports'].items():
        cmdline += ' -p {0}:{1}'.format(p_host,p_cont)

cmdline += ' {0}'.format(image)
if args.filename is not None:
    cmdline += ' {0}'.format(args.filename)

print cmdline
