#!/usr/bin/env python
import sys
import os

from dockeri import main

if __name__ == '__main__':
    out = main(sys.argv[1:])
    if out == os.EX_CONFIG:
        sys.exit(os.EX_OK)
    sys.exit(out)
