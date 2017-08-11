# coding=utf-8

from qtpy import QtCore
from qtpip import contextmenu, _
from datamatrix import DataMatrix
from qdatamatrix import QDataMatrix


class QPackageMatrix(QDataMatrix):

	def __init__(self, qpipwidget):

		self._qpipwidget = qpipwidget
		dm = DataMatrix()
		dm.package = u''
		dm.installed_version = u''
		dm.latest_version = u''
		QDataMatrix.__init__(self, dm)
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
		self._qpipwidget._cancelled = False
		for i, pkg in enumerate(pkglist):
			names.append(pkg.name)
			installed_versions.append(pkg.installed_version)
			latest_versions.append(
				pkg.latest_version if pkg.latest_version_known else u'?')
			self._qpipwidget.ui.label_progress.setText(
				_(u'Discovered %d package(s) (%s)') % (i+1, pkg.name))
			QtCore.QCoreApplication.processEvents()
			if self._qpipwidget._cancelled:
				break
		self._dm.length = len(names)
		self._dm.package = names
		self._dm.installed_version = installed_versions
		self._dm.latest_version = latest_versions
		self.refresh()
		self._spreadsheet.show()
		self._qpipwidget.ui.button_cancel.hide()
		self._qpipwidget.ui.searchbox.setDisabled(False)
		self._qpipwidget.ui.button_search.setDisabled(False)
		self._qpipwidget.ui.button_show_installed.setDisabled(False)
		self._qpipwidget.ui.button_show_updates.setDisabled(False)
		
	def refresh(self):
		
		QDataMatrix.refresh(self)
		self._spreadsheet.setRowCount(len(self._dm)+1)
		self._spreadsheet.setColumnCount(3)
		self._qpipwidget.ui.label_progress.hide()		

	def refresh_pkginfo(self, pkg):
		
		for row in self.dm:
			if row.package != pkg.name:
				continue
			pkg.clear_cache()
			row.installed_version = pkg.installed_version
			row.latest_version = pkg.latest_version
			self.refresh()