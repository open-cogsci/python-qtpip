# coding=utf-8

from __future__ import unicode_literals
import os
from qtpy import QtWidgets, uic
from qtpip import PackageManager, QPackageMatrix, decorators


class QPipWidget(QtWidgets.QWidget):

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
		self.ui.button_show_available.clicked.connect(self.show_available)
		self.ui.button_cancel.clicked.connect(self._set_cancelled)
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

	@decorators.may_take_time
	def show_available(self, *args):

		self.ui.qdm.set_pkglist(self.pm.available)
