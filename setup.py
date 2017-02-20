#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='c2artmc',
      version='1.0',
      description="Compiler from C to ARTMC",
      author='Matej Marusak',
      author_email='marusak.matej@gmail.com',
      url='https://github.com/mmarusak/C2ARTMC',
      license='MIT',
      packages=['src'],
      setup_requires=['setuptools',
                      ],
      tests_require=['pytest'],
      )
