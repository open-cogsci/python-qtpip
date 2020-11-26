#!/usr/bin/env python
# coding=utf-8

"""
This file is part of QtPip.

QtPip is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

QtPip is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with QtPip.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup


def data_files():

	return [
		("share/opensesame_extensions/package_manager", [
			'opensesame_extensions/package_manager/info.yaml',
			'opensesame_extensions/package_manager/package_manager.py'
			]),
		]

setup(
	name="python-qtpip",
	version='0.2.0',
	description="A graphical manager for PyPi plus an OpenSesame extension",
	author="Sebastiaan Mathot",
	author_email="s.mathot@cogsci.nl",
	url="https://github.com/smathot/python-qtpip",
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: MacOS X',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	entry_points={
		'console_scripts': [
			'qtpip = qtpip.__main__:main'
		]
	},
	install_requires=[
		'yolk3k',
		'python-qdatamatrix'
		],
	include_package_data=True,
	packages = ['qtpip'],
	data_files=data_files()
	)
