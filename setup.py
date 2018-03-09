#!/usr/bin/env python
from setuptools import find_packages, setup

import versioneer

# Set affiliated package-specific settings
PACKAGENAME = 'dockeri'
DESCRIPTION='Multiplatform CLI for Docker'

AUTHOR = 'Carlos H. Brandt'
AUTHOR_EMAIL = 'carlos.brandt@ssdc.asi.it'
LICENSE = 'GPL'
URL = 'https://github.com/chbrandt/docker_interface'

# Treat everything in scripts except README.rst as a script to be installed
scripts = [fname for fname in glob.glob(os.path.join('scripts', '*'))]

packages = find_packages()

setup(name=PACKAGENAME,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description=DESCRIPTION,
      packages=find_packages(),
      scripts=scripts,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      url=URL,
      zip_safe=False,
      use_2to3=True
)