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
from qtpip._package import Package
from qtpip import utils
from yolk import pypi, yolklib


class PackageManager(object):

    def __init__(self):

        self._cheeseshop = pypi.CheeseShop()

    def package(self, pkg):

        return Package(self, pkg)

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

        for name in utils.search_pypi(*query.lower().split()):
            yield Package(self, name)
