#!/usr/bin/env python3

import setuptools
from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(name="WoRMStools",
      version='1.3',
      long_description = readme,
      long_description_content_type='text/markdown',
      author='Ulises Rosas',
      author_email='ulisesfrosasp@gmail.com',
      url='https://github.com/Ulises-Rosas/WoRMStools',
      packages = ['WoRMStools'],
      package_dir = {'WoRMStools': 'src'},
      scripts = ['src/worms.py'],
      setup_requires=['wheel'],
      classifiers=['Programming Language :: Python :: 3']
      )

