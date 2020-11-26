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

import os
from qtpip import utils, _
from yolk import yolklib

LATEST_VERSION_UNKNOWN = _(u'Right-click to check')
INSTALLED_VERSION_NOT_INSTALLED = _(u'Not installed')
LOCATION_NOT_INSTALLED = _(u'Not installed')


class Package(object):

    def __init__(self, packagemanager, name, version=None, location=None):

        self._packagemanager = packagemanager
        self._name = name
        self._version = version
        self._location = location
        self._latest_version = None

    def __str__(self):

        return '- %s: %s' % (self.name, self.installed_version)

    def __eq__(self, other):

        return self.name == other.name

    @staticmethod
    def from_dist(packagemanager, dist):

        return Package(packagemanager, name=dist.project_name,
            version=dist.version, location=dist.location)

    @property
    def location(self):

        if self._location is None:
            try:
                dist, active = yolklib.get_distributions(
                    'active', self._name).send(None)
            except StopIteration:
                self._location = LOCATION_NOT_INSTALLED
            else:
                self._location = dist.location
        return self._location

    @property
    def name(self):

        return self._name

    @property
    def installed_version(self):

        if self._version is None:
            try:
                self._version = yolklib.get_highest_installed(self.name)
            except IndexError:
                self._version = INSTALLED_VERSION_NOT_INSTALLED
        return self._version

    @property
    def latest_version_known(self):

        return self._latest_version is not None

    @property
    def latest_version(self):

        if self._latest_version is None:
            try:
                l = self._packagemanager._cheeseshop.package_releases(self.name)
            except BaseException:
                self._latest_version = LATEST_VERSION_UNKNOWN
            else:
                self._latest_version = l[0] if l else LATEST_VERSION_UNKNOWN
        return self._latest_version

    @property
    def is_latest(self):

        return not (self.latest_version != LATEST_VERSION_UNKNOWN \
            and self.installed_version != INSTALLED_VERSION_NOT_INSTALLED \
            and self.latest_version != self.installed_version)

    @property
    def is_installed(self):

        return self.installed_version not in \
            (None, INSTALLED_VERSION_NOT_INSTALLED)

    @property
    def is_writable(self):

        return os.path.exists(self.location) \
            and os.access(self.location, os.W_OK)

    def uninstall(self):

        """
        desc:
            Uninstalls the current package.

        returns:
            A (bool, str) tuple where the bool indicates if the operation was
            successfull, and the str contains the output of pip.
        """

        self.clear_cache()
        return utils.pipcmd('uninstall', '-y', self.name)

    def install(self, version=None):

        """
        desc:
            Installs the current package.

        keywords:
            version:
                desc:	A version string to install another version than the
                        latest.
                type:	[None, str]

        returns:
            A (bool, str) tuple where the bool indicates if the operation was
            successfull, and the str contains the output of pip.
        """

        self.clear_cache()
        if version is None:
            return utils.pipcmd('install', self.name)
        return utils.pipcmd('install', '%s==%s' % (self.name, version))

    def clear_cache(self):

        """
        desc:
            Clears the package cache.
        """

        self._version = self._latest_version = self._location = None
