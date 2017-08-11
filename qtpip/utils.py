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

from __future__ import unicode_literals
import sys
import pip
try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO
try:
	from urllib.request import urlopen
except ImportError:
	from urllib import urlopen

TMPL_URL_PKGINFO = 'https://pypi.python.org/pypi?name=%s&:action=display_pkginfo'
REGEX_PKGINFO = r'^(?P<pkg>[a-zA-Z0-9_\-.]+) \((?P<version>[a-zA-Z0-9_\-.]+)\)'
REGEX_PKGINFO_VERSION = r'^Version: (?P<version>[a-zA-Z0-9_\-.]+)$'


def pipcmd(*cmd):

	_stdout = sys.stdout
	sys.stdout = StringIO()
	success = not bool(pip.main(list(cmd)))
	output = sys.stdout.getvalue()
	sys.stdout = _stdout
	return success, output


def urlread(url):

	fd = urlopen(url)
	return fd.read().decode('utf-8')
