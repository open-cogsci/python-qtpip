# coding=utf-8

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
		

class QInstallAction(QPackageAction):

	def __init__(self, menu):

		QPackageAction.__init__(self, u'system-software-install',
			_(u'Install'), menu)

	@decorators.may_take_time
	def activate(self, *args):

		self.qpackagematrix.log(self._pkg.install()[1])
		self.qpackagematrix.refresh_pkginfo(self._pkg)


class QUninstallAction(QPackageAction):

	def __init__(self, menu):

		QPackageAction.__init__(self, u'list-remove',
			_(u'Uninstall'), menu)

	@decorators.may_take_time
	def activate(self, *args):

		self.qpackagematrix.log(self._pkg.uninstall()[1])
		self.qpackagematrix.refresh_pkginfo(self._pkg)


class QUpdateAction(QPackageAction):

	def __init__(self, menu):

		QPackageAction.__init__(self, u'system-software-update',
			_(u'Update'), menu)

	@decorators.may_take_time
	def activate(self, *args):

		self.qpackagematrix.log(
			self._pkg.install(version=self._pkg.latest_version)[1])
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
