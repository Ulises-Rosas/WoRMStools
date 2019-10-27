#!/usr/bin/env python3

import setuptools
from distutils.core import setup

setup(name="WoRMStools",
      version='1.0',
      author='Ulises Rosas',
      author_email='ulisesfrosasp@gmail.com',
      url='https://github.com/Ulises-Rosas/OBISdat',
      packages = ['WoRMStools'],
      package_dir = {'WoRMStools': 'src'},
      scripts = ['src/worms.py'],
      setup_requires=['wheel']
      )

