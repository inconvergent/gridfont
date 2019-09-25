#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


setup(name='font',
      version='0.5.2',
      description='',
      url='https://github.com/inconvergent/gridfont',
      license='MIT License',
      author='Anders Hoff',
      author_email='inconvergent@gmail.com',
      install_requires=['docopt', 'svgwrite'],
      packages=find_packages(),
      entry_points={'console_scripts': ['gridfont=gridfont:main']},
      zip_safe=True
      )

