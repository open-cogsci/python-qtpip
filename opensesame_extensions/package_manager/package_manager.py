# coding=utf-8

from libopensesame.py3compat import *
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'package_manager', category=u'extension')


class package_manager(base_extension):

	def activate(self):
		
		from qtpip._qpipwidget import QPipWidget
		
		if not hasattr(self, '_qpipwidget'):
			self._qpipwidget = QPipWidget()
			self._qpipwidget.log = self._log
		self.tabwidget.add(self._qpipwidget, u'system-software-install',
			_(u'Package manager'))
			
	def _log(self, msg):
		
		self.console.write(msg + u'\n')
