#!/usr/bin/env python
from setuptools import find_packages, setup

NAME = 'jupyter_spaces'
VERSION = '0.1.0'
AUTHOR = 'Davide Sarra'
URL = 'https://github.com/davidesarra/jupyter_spaces'
DESCRIPTION = 'Create parallel namespaces in Jupyter Notebooks'
LICENSE = 'MIT'
CLASSIFIERS = [
    'Environment :: Console',
    'Framework :: IPython',
    'Framework :: Jupyter',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]
KEYWORDS = 'jupyter ipython magic extension namespace'

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

REQUIREMENTS = [
    'ipython>=5.0.0',
]

if __name__ == "__main__":
    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        url=URL,
        license=LICENSE,
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(exclude=['tests']),
        install_requires=REQUIREMENTS,
        python_requires='~=3.4',
    )
