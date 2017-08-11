# coding=utf-8

from __future__ import unicode_literals
from qtpip._package import Package
from yolk import pypi, yolklib
	
	
class PackageManager(object):

	def __init__(self):

		self._cheeseshop = pypi.CheeseShop()

	def package(self, pkg):

		return Package(self, pkg)

	@property
	def available(self):

		for name in self._cheeseshop.pkg_list:
			yield Package(self, name)

	@property
	def installed(self):
		
		names = []
		for dist, active in yolklib.get_distributions('active'):
			if dist.project_name in names:
				continue
			names.append(dist.project_name)
			yield Package.from_dist(self, dist)

	@property
	def outdated(self):

		for pkg in self.installed:
			if not pkg.is_latest:
				yield pkg

	def search(self, query):

		lquery = query.lower().split()
		for pkg in self.available:
			if all(q in pkg.name.lower() for q in lquery):
				yield pkg
