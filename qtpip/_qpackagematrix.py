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

from qtpy import QtCore
from qtpip import contextmenu, _
from qtpip._package import LATEST_VERSION_UNKNOWN
from datamatrix import DataMatrix
from qdatamatrix import QDataMatrix


class QPackageMatrix(QDataMatrix):

    def __init__(self, qpipwidget):

        self._qpipwidget = qpipwidget
        dm = DataMatrix()
        dm.package = u''
        dm.installed_version = u''
        dm.latest_version = u''
        dm.location = u''
        QDataMatrix.__init__(self, dm, read_only=True)
        self._spreadsheet.verticalHeader().hide()
        self._spreadsheet.contextMenuEvent = self.context_menu

    @property
    def log(self):

        return self._qpipwidget.log

    def context_menu(self, e):

        contextmenu.QPackageMenu(self).exec_(e.globalPos())

    def set_pkglist(self, pkglist):

        self._qpipwidget.ui.label_progress.show()
        self._qpipwidget.ui.button_cancel.show()
        self._qpipwidget.ui.searchbox.setDisabled(True)
        self._qpipwidget.ui.button_search.setDisabled(True)
        self._qpipwidget.ui.button_show_installed.setDisabled(True)
        self._qpipwidget.ui.button_show_updates.setDisabled(True)
        self._spreadsheet.hide()
        self._qpipwidget.ui.label_progress.setText(_(u'Refreshing …'))
        QtCore.QCoreApplication.processEvents()
        names = []
        installed_versions = []
        latest_versions = []
        locations = []
        self._qpipwidget._cancelled = False
        for i, pkg in enumerate(pkglist):
            names.append(pkg.name)
            installed_versions.append(pkg.installed_version)
            latest_versions.append(pkg.latest_version \
                if pkg.latest_version_known else LATEST_VERSION_UNKNOWN)
            locations.append(pkg.location)
            self._qpipwidget.ui.label_progress.setText(
                _(u'Discovered %d package(s) (%s)') % (i+1, pkg.name))
            QtCore.QCoreApplication.processEvents()
            if self._qpipwidget._cancelled:
                break
        self._dm.length = len(names)
        self._dm.package = names
        self._dm.installed_version = installed_versions
        self._dm.latest_version = latest_versions
        self._dm.location = locations
        self.refresh()
        self._spreadsheet.show()
        self._qpipwidget.ui.button_cancel.hide()
        self._qpipwidget.ui.searchbox.setDisabled(False)
        self._qpipwidget.ui.button_search.setDisabled(False)
        self._qpipwidget.ui.button_show_installed.setDisabled(False)
        self._qpipwidget.ui.button_show_updates.setDisabled(False)

    def refresh(self):

        QDataMatrix.refresh(self)
        self._qpipwidget.ui.label_progress.hide()

    def refresh_pkginfo(self, pkg):

        for row in self.dm:
            if row.package != pkg.name:
                continue
            pkg.clear_cache()
            row.installed_version = pkg.installed_version
            row.latest_version = pkg.latest_version
            row.location = pkg.location
            self.refresh()
