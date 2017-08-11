# coding=utf-8

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
