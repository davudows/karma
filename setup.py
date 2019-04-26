#!/usr/bin/env python3

from setuptools import setup, find_packages
from karma.version import __version__, __author__, __email__, __license__

import os

try:
    long_description = open('README.md', 'rt').read()
except Exception as e:
    long_description = 'Find leaked emails with your passwords.'


def read_requirements():
    """Parse requirements from requirements.txt."""
    requirements_path = os.path.join('.', 'requirements.txt')
    with open(requirements_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements


setup(
    name                = 'karma',
    version             = __version__,
    description         = 'Find leaked emails with your passwords.',
    long_description    = long_description,
    author              = __author__,
    author_email        = __email__,
    url                 = 'https://github.com/decoxviii/karma',
    packages            = find_packages(),
    scripts             = ['bin/karma'],
    license             = __license__,
    install_requires    = read_requirements(),
    classifiers = [
        'Programming Language :: Python3',
        'License :: MIT',
        'Environment :: Console',
    ],
)

