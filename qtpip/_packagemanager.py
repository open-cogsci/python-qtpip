# coding=utf-8

from __future__ import unicode_literals
from qtpip._package import Package
import re
import sys
import pip
from yolk import pypi, yolklib
try:
	# Python 2
	from StringIO import StringIO
except ImportError:
	# Python 3
	from io import StringIO
	
	
class PackageManager(object):

	def __init__(self):

		self._cheeseshop = pypi.CheeseShop()
		self.pkg_list_pypi = self._cheeseshop.pkg_list

	def package(self, pkg):

		return Package(self, pkg)

	@property
	def available(self):

		for name in self._cheeseshop.pkg_list:
			yield Package(self, name)

	@property
	def installed(self):

		for pkg in yolklib.get_packages('all'):
			yield Package(self, pkg.project_name, pkg.version)

	@property
	def outdated(self):

		for pkg in self.installed:
			if not pkg.is_latest:
				yield pkg

	def search(self, query):

		hits = []
		lquery = query.split()
		for pkg in self.available:
			for q in lquery:
				if q not in pkg.name:
					break
			else:
				hits.append(pkg)
		return hits

	def pip_cmd(self, *cmd):

		_stdout = sys.stdout
		sys.stdout = StringIO()
		if pip.main(list(cmd)):
			raise Exception('pip command failed: %s' % ' '.join(cmd))
		output = sys.stdout.getvalue()
		sys.stdout = _stdout
		return output
