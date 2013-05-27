#!/usr/bin/env python

from distutils.core import setup

import libsubte

setup(name = 'subte',
      version = libsubte.__version__,
      description = 'Program and library for managing and generating GTFS (General Transit Feed Specification) data',
      long_description = 'subte is an interface for managing public transit data. It can collect stops, create routes and timetables, and export to GTFS which can be used by google transit or other routing applications like Open Trip Planner.',
      license = 'GPLv3',
      author = 'Marcus Dillavou',
      author_email = 'line72@line72.net',
      url = 'http://line72.net/index.php/software/subte/',
      packages = ['libsubte', 'libsubte.interface'],
      scripts = ['subte'],
      data_files = [('share/subte', ['AUTHORS', 'ChangeLog', 'COPYING', 'README']),
                    ('share/applications', ['subte.desktop']),
                    ('share/icons', ['images/subte.svg']),
                    ],

      )
