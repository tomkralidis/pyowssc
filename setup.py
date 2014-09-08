# -*- coding: iso-8859-15 -*-

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

