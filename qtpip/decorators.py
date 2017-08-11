# coding=utf-8

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
