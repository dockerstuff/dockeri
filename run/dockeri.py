#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser(description='Interface for Docker containers.')

parser.add_argument('image', choices=['annz','ds9','browse','asdcbibtool'],
        help='alias/name of the image to run.')

parser.add_argument('-i','--input',dest='input_dir',default=None,
        help='host directory to use as input for the container')

parser.add_argument('-o','--output',dest='output_dir',default=None,
        help='host directory to use as output for the container')

parser.add_argument('-f','--file',dest='filename',
        help='filename (found inside input-dir) to argument the container entrypoint')

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
idir_cfg = cfg['volumes']['input'] if args.input_dir is None else args.input_dir
idir_cfg = os.path.abspath(idir_cfg)
odir_cfg = cfg['volumes']['output'] if args.output_dir is None else args.output_dir
odir_cfg = os.path.abspath(odir_cfg)
cmdline += ' -v {0}:{1}'.format(idir_cfg,'/data/input')
cmdline += ' -v {0}:{1}'.format(odir_cfg,'/data/output')

# option for accessing the x11
if args.with_x11:
    import x11
    _x11 = '/tmp/.X11-unix'
    _dsp = x11.get_DISPLAY()
    cmdline += ' -v {0}:{1} -e DISPLAY={2}'.format(_x11,_x11,_dsp)

cmdline += ' {0}'.format(image)
if args.filename is not None:
    cmdline += ' {0}'.format(args.filename)

print cmdline
