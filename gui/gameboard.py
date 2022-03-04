from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from tile import Tile

class Board(QWidget):
	def __init__(self, parent = None):
		super(Board, self).__init__(parent)
		self.setMinimumSize(490, 490)
		self.tiles = []

	def load(self):
		for x in range(7):
			l = []
			for y in range(7):
				t = Tile(self)
				t.move(x*70, y*70)
				l.append(t)
			self.tiles.append(l)

	def resizeEvent(self, event):
		w = (event.size().width() - 490)/2
		h = (event.size().height() - 490)/2

		#Move all tiles according to the new size.
		for x in range(7):
			for y in range(7):
				self.tiles[x][y].move(x*70+w, y*70+h)
		super(Board, self).resizeEvent(event)