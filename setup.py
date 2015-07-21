#!/usr/bin/env python
"""Version information:

IPython extension command for displaying version information about selected
Python modules.
"""

DOCLINES = __doc__.split('\n')

CLASSIFIERS = """\
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 3
Operating System :: MacOS
Operating System :: POSIX
Operating System :: Unix
Operating System :: Microsoft :: Windows
"""

import os
from setuptools import setup

NAME = "version_information"
MAJOR = 1
MINOR = 0
MICRO = 3 
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
AUTHOR = "J. Robert Johansson"
AUTHOR_EMAIL = "jrjohansson@gmail.com"
LICENSE = "BSD"
DESCRIPTION = DOCLINES[0]
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])
URL = "https://github.com/jrjohansson/version_information"
PLATFORMS = ["Linux", "Mac OSX", "Unix", "Windows"]

def write_version_py(filename=NAME+'/version.py'):
    cnt = """\
# THIS FILE IS GENERATED FROM SETUP.PY
version = '%(version)s'
"""
    with open(filename, 'w') as f:
        f.write(cnt % {'version': VERSION})

write_version_py()

setup(
    name=NAME,
    version=VERSION,
    packages=["version_information"],
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    platforms=PLATFORMS,
)
