from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Tile(QLabel):
	def __init__(self, parent = None):
		super(Tile, self).__init__(parent)
		self.setFixedSize(70, 70)
		self.setFrameStyle(QFrame.Box | QFrame.Raised)
		self.setLineWidth(1)
		self.setMidLineWidth(3)
		self.setMouseTracking(True)
		self.setText("A")
