#!/usr/bin/env python

from setuptools import setup
from pyreadme import __version__

setup(
      name='pyreadme',
      version=__version__,
      description='Simple markdown editor written in PyQt4',
      keywords='pyqt pyqt4 markdown-editor',
      url='http://github.com/ksharindam/pyreadme',
      author='Arindam Chaudhuri',
      author_email='ksharindam@gmail.com',
      license='GPLv3',
      packages=['pyreadme'],
#      install_requires=['PyQt4',      ],
      entry_points={
          'console_scripts': ['pyreadme=pyreadme.main:main'],
      },
#      include_package_data=True,
      zip_safe=False)
