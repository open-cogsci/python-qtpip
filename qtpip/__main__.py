#!/usr/bin/env python
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

import sys
from qtpy import QtWidgets
from qtpip._qpipwidget import QPipWidget


def main():

    app = QtWidgets.QApplication(sys.argv)
    w = QPipWidget()
    w.resize(1000, 600)
    w.move(300, 300)
    w.setWindowTitle('Python Package Manager')
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
