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

from qtpy import QtWidgets, QtGui
from qtpip import decorators, _


class QPackageAction(QtWidgets.QAction):

    def __init__(self, icon, title, menu, keyseq=None):

        QtWidgets.QAction.__init__(self, QtGui.QIcon.fromTheme(icon), title,
            menu)
        self._menu = menu
        self._pkg = menu.pkg
        if keyseq is not None:
            self.setShortcut(QtGui.QKeySequence(keyseq))
        self.triggered.connect(self.activate)
        
    @property
    def qpackagematrix(self):
        
        return self._menu._qpackagematrix

    @property
    def qpipwidget(self):
        
        return self._menu._qpackagematrix._qpipwidget
        

class QInstallAction(QPackageAction):

    def __init__(self, menu):

        QPackageAction.__init__(self, u'system-software-install',
            _(u'Install'), menu)

    @decorators.may_take_time
    def activate(self, *args):

        success, output = self._pkg.install()
        if success:
            self.qpipwidget.installed.emit(self._pkg.name)
        else:
            self.qpipwidget.install_failed.emit(self._pkg.name)
        self.qpackagematrix.log(output)
        self.qpackagematrix.refresh_pkginfo(self._pkg)


class QUninstallAction(QPackageAction):

    def __init__(self, menu):

        QPackageAction.__init__(self, u'list-remove',
            _(u'Uninstall'), menu)

    @decorators.may_take_time
    def activate(self, *args):

        success, output = self._pkg.uninstall()
        if success:
            self.qpipwidget.uninstalled.emit(self._pkg.name)
        else:
            self.qpipwidget.uninstall_failed.emit(self._pkg.name)
        self.qpackagematrix.log(output)
        self.qpackagematrix.refresh_pkginfo(self._pkg)


class QUpdateAction(QPackageAction):

    def __init__(self, menu):

        QPackageAction.__init__(self, u'system-software-update',
            _(u'Update'), menu)

    @decorators.may_take_time
    def activate(self, *args):

        success, output = self._pkg.install(version=self._pkg.latest_version)
        if success:
            self.qpipwidget.installed.emit(self._pkg.name)
        else:
            self.qpipwidget.install_failed.emit(self._pkg.name)
        self.qpackagematrix.log(output)
        self.qpackagematrix.refresh_pkginfo(self._pkg)


class QPackageMenu(QtWidgets.QMenu):

    @decorators.may_take_time
    def __init__(self, qpackagematrix=None):

        QtWidgets.QMenu.__init__(self, parent=qpackagematrix._spreadsheet)
        self._qpackagematrix = qpackagematrix
        row = self._qpackagematrix._spreadsheet.currentRow()-1
        if row < 0:
            return
        self.pkg = self._qpackagematrix._qpipwidget.pm.package(
            self._qpackagematrix.dm[row].package)
        self._qpackagematrix.refresh_pkginfo(self.pkg)
        if not self.pkg.is_installed:
            self.addAction(QInstallAction(self))
            return
        if not self.pkg.is_latest:
            self.addAction(QUpdateAction(self))
        if self.pkg.is_writable:
            self.addAction(QUninstallAction(self))
