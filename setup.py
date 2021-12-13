#!/usr/bin/env python3
# coding:utf-8
from distutils.core import setup

setup(
  name='dirtybiologystan_flag_api',
  packages=['dirtybiologystan_flag_api'],
  version='1.4',
  license='gpl-3.0',
  description="An API that get infos about pixels of the https://fouloscopie.com/experiment/7 's flag",
  author='Jean Dubois',
  author_email='jd-dev@laposte.net',
  url='https://github.com/jd-develop/dirtybiologystan_flag_api',
  download_url='https://github.com/jd-develop/dirtybiologystan_flag_api/archive/refs/tags/1.4.tar.gz',
  keywords=['DIRTYBIOLOGYSTAN'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
