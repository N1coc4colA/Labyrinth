from PyQt5.QtGui import QPixmap

class TestData:
	def __init__(self, o = 0):
		self.orientation = o
		self.pixmap = QPixmap()
		self.player = []

	def getId(self):
		return 0