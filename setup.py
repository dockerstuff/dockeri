#!/usr/bin/env python
from setuptools import find_packages, setup
import glob
import os

import versioneer

PACKAGENAME = 'dockeri'
DESCRIPTION='Multiplatform CLI for Docker'

AUTHOR = 'Carlos H. Brandt'
AUTHOR_EMAIL = 'carlos.brandt@ssdc.asi.it'
LICENSE = 'GPL'
URL = 'https://github.com/chbrandt/docker_interface'

scripts = [fname for fname in glob.glob(os.path.join('bin', '*'))]

setup(name=PACKAGENAME,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description=DESCRIPTION,
      packages=['dockeri'],
      package_data={'dockeri':['conf.d/*.cfg']},
      scripts=scripts,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      url=URL
)
