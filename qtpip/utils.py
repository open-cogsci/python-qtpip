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
try:
	import pip._internal as pipmain
except ImportError:
	import pip as pipmain
try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO
try:
	from urllib.request import urlopen
except ImportError:
	from urllib import urlopen


def pipcmd(*cmd):

	_stdout = sys.stdout
	sys.stdout = StringIO()
	success = not bool(pipmain.main(list(cmd)))
	output = sys.stdout.getvalue()
	sys.stdout = _stdout
	return success, output


def urlread(url):

	fd = urlopen(url)
	return fd.read().decode('utf-8')


def search_pypi(*query):

	if len(query) > 1:
		results = set(search_pypi(query[0]))
		for q in query[1:]:
			if not results:
				return
			results &= set(search_pypi(q))
		return sorted(results)
	success, output = pipcmd('search', query[0])
	if not success:
		return
	packages = []
	for line in output.split('\n'):
		if not line or line.startswith(' '):
			continue
		lst = line.split(' ')
		if not lst:
			continue
		packages.append(lst[0])
	return sorted(packages)
