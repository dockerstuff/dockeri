#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser(description='Interface for Docker containers.')

parser.add_argument('image', choices=['annz','ds9','browse'],
        help='alias/name of the image to run.')

parser.add_argument('-i','--input',dest='input_dir',default='$PWD/input',
        help='host directory to use as input for the container')

parser.add_argument('-o','--output',dest='output_dir',default='$PWD/output',
        help='host directory to use as output for the container')

parser.add_argument('-f','--file',dest='filename',
        help='filename (found inside input-dir) to argument the container entrypoint')

parser.add_argument('-x',dest='with_x11',action='store_true',
        help='route x11 from the container?')

args = parser.parse_args()

cmdline = 'docker run -it'

# image name at Hub
imagehub = 'chbrandt/{0}'.format(args.image)

# i/o volumes
cmdline += ' -v {0}:{1}'.format(args.input_dir,'/data/input')
cmdline += ' -v {0}:{1}'.format(args.output_dir,'/data/output')

# option for accessing the x11
if args.with_x11:
    import x11
    _x11 = '/tmp/.X11-unix'
    _dsp = x11.get_DISPLAY()
    cmdline += ' -v {0}:{1} -e DISPLAY={2}'.format(_x11,_x11,_dsp)

cmdline += ' {0}'.format(imagehub)
if args.filename is not None:
    cmdline += ' {0}'.format(args.filename)

print cmdline

