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
from qtpy import QtWidgets, uic, QtCore
from qtpip import PackageManager, QPackageMatrix, decorators


class QPipWidget(QtWidgets.QWidget):

    installed = QtCore.Signal('QString')
    uninstalled = QtCore.Signal('QString')
    install_failed = QtCore.Signal('QString')
    uninstall_failed = QtCore.Signal('QString')

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent=parent)
        self.pm = PackageManager()
        ui_path = os.path.join(
            os.path.dirname(__file__), u'data', u'pipwidget.ui')
        with open(ui_path) as fd:
            self.ui = uic.loadUi(fd, self)
        self.ui.searchbox.editingFinished.connect(self.search)
        self.ui.button_show_installed.clicked.connect(self.show_installed)
        self.ui.button_show_updates.clicked.connect(self.show_updates)
        self.ui.button_cancel.clicked.connect(self._set_cancelled)
        self.ui.button_cancel.hide()
        self.ui.qdm = QPackageMatrix(self)
        self.ui.vbox.addWidget(self.ui.qdm)

    def log(self, msg):

        print(msg)

    def _set_cancelled(self):

        self._cancelled = True

    @decorators.may_take_time
    def search(self):

        query = self.ui.searchbox.text()
        if len(query) < 3:
            return
        self.ui.qdm.set_pkglist(self.pm.search(query))

    @decorators.may_take_time
    def show_installed(self, *args):

        self.ui.qdm.set_pkglist(self.pm.installed)

    @decorators.may_take_time
    def show_updates(self, *args):

        self.ui.qdm.set_pkglist(self.pm.outdated)
