# coding=utf-8

from libopensesame.py3compat import *
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'package_manager', category=u'extension')


class package_manager(base_extension):

    def event_startup(self):

        self._initialized = False

    def init(self):

        from qtpip._qpipwidget import QPipWidget
        self._qpipwidget = QPipWidget()
        self._qpipwidget.log = self._log
        self._qpipwidget.installed.connect(
            lambda pkg: self.extension_manager.fire(
            'notify', message='Installed %s' % pkg))
        self._qpipwidget.uninstalled.connect(
            lambda pkg: self.extension_manager.fire(
            'notify', message='Uninstalled %s' % pkg))
        self._qpipwidget.install_failed.connect(
            lambda pkg: self.extension_manager.fire(
            'notify', message='Failed to installed %s' % pkg,
            category='warning'))
        self._qpipwidget.uninstall_failed.connect(
            lambda pkg: self.extension_manager.fire(
            'notify', message='Uninstalled %s' % pkg,
            category='warning'))
        self._initialized = True

    def activate(self):

        if not self._initialized:
            self.init()
        self.tabwidget.add(self._qpipwidget, u'system-software-install',
            _(u'Python package manager'))

    def _log(self, msg):

        self.console.write(msg + u'\n')
