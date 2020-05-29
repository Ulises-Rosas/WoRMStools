#!/usr/bin/env python3

import setuptools
from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(name="wormstools",
      version='1.3.4',
      description="Wrapper for WoRMS Rest API",
      long_description = readme,
      long_description_content_type='text/markdown',
      author='Ulises Rosas',
      author_email='ulisesfrosasp@gmail.com',
      url='https://github.com/Ulises-Rosas/WoRMStools',
      packages = ['wormstools'],
      package_dir = {'wormstools': 'src'},
      entry_points={
        'console_scripts': [
            'worms = wormstools.worms:main'
            ]
      },
      classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License'
            ]

      )
