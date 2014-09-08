# -*- coding: iso-8859-15 -*-
# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2011 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

from distutils.core import setup
import os

from pyowssc import __version__ as version

# set dependencies
INSTALL_REQUIRES = [line.strip() for line in open('requirements.txt')]

KEYWORDS = [
    'OGC',
    'health check',
    'OWS',
    'status checker',
]

DESCRIPTION = 'Python OGC Web Service Status Checker'

CONTACT = 'Tom Kralidis'

EMAIL = 'tomkralidis@gmail.com'

SCRIPTS = [os.path.join('bin', 'pyowssc-admin.py')]

URL = 'https://github.com/tomkralidis/pyowssc'


# from https://wiki.python.org/moin/Distutils/Cookbook/AutoPackageDiscovery
def is_package(path):
    """decipher whether path is a Python package"""
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )


def find_packages(path, base=""):
    """Find all packages in path"""
    packages = {}
    for item in os.listdir(path):
        dir1 = os.path.join(path, item)
        if is_package(dir1):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir1
            packages.update(find_packages(dir1, module_name))
    return packages

setup(
    name='pyowssc',
    version=version,
    description=DESCRIPTION.strip(),
    long_description=open('README.md').read(),
    license='MIT',
    platforms='all',
    keywords=' '.join(KEYWORDS),
    author=CONTACT,
    author_email=EMAIL,
    maintainer=CONTACT,
    maintainer_email=EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages('.'),
    #package_data=PACKAGE_DATA,
    scripts=SCRIPTS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Atmospheric Science'
    ]
)

