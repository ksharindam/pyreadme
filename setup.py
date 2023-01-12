from setuptools import setup
from pyreadme import __version__

setup(
      name='pyreadme',
      version=__version__,
      description='Simple markdown editor written in PyQt',
      long_description='Simple markdown editor written in PyQt',
      keywords='pyqt markdown-editor',
      url='http://github.com/ksharindam/pyreadme',
      author='Arindam Chaudhuri',
      author_email='ksharindam@gmail.com',
      license='GPLv3',
      install_requires=['markdown'],
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: X11 Applications :: Qt',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 3.7',
      ],
      packages=['pyreadme'],
      entry_points={
          'console_scripts': ['pyreadme=pyreadme.main:main'],
      },
      data_files=[
                 ('share/applications', ['files/pyreadme.desktop']),
      ],
      include_package_data=True,
      zip_safe=False)
