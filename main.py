from PyQt5.QtWidgets import QApplication
from gameboard import Board

if __name__ == '__main__':
	import sys
	#Setup the app and show the window.
	app = QApplication(sys.argv)
	b = Board()
	b.load()
	b.show()
	sys.exit(app.exec_())