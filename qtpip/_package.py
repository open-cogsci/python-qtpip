# coding=utf-8

from __future__ import unicode_literals
from qtpip import utils, _
from yolk import yolklib


class Package(object):

	def __init__(self, packagemanager, name, version=None):

		self._packagemanager = packagemanager
		self._name = name
		self._version = version
		self._latest_version = None

	def __str__(self):

		return '- %s: %s' % (self.name, self.installed_version)

	def __eq__(self, other):

		return self.name == other.name
		
	def clear_cache(self):
		
		self._version = self._latest_version = None

	@property
	def name(self):

		return self._name

	@property
	def installed_version(self):

		if self._version is None:
			try:
				self._version = yolklib.get_highest_installed(self.name)
			except:
				self._version = _(u'Not installed')
		return self._version
		
	@property
	def latest_version_known(self):
		
		return self._latest_version is not None

	@property
	def latest_version(self):

		if self._latest_version is None:
			l = self._packagemanager._cheeseshop.package_releases(self.name)
			if l:
				self._latest_version = l[0]
			else:
				self._latest_version = '?'
		return self._latest_version

	@property
	def is_latest(self):

		return not (self.latest_version != '?' and self.installed_version != '?' \
			and self.latest_version != self.installed_version)

	@property
	def is_installed(self):

		return self.installed_version not in (None, _(u'Not installed'))

	def uninstall(self):

		return utils.pipcmd('uninstall', '-y', self.name)

	def install(self, version=None):

		if version is None:
			return utils.pipcmd('install', self.name)
		return utils.pipcmd('install', '%s==%s' % (self.name, version))
