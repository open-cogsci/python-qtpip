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

from qtpy import QtWidgets, QtGui, QtCore


def may_take_time(fnc):
    
    def inner(*args, **kwargs):
        
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(
            QtCore.Qt.WaitCursor))
        QtWidgets.QApplication.processEvents()
        retval = fnc(*args, **kwargs)
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QApplication.processEvents()
        return retval
        
    return inner
