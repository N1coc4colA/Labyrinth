from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from gui.tile import Tile, InputTile

class TestData:
	def __init__(self, o = 0):
		self.orientation = o

class Board(QWidget):
	def __init__(self, parent = None):
		super(Board, self).__init__(parent)
		self.setMinimumSize(630, 630)
		self.tiles = []
		self.input_tiles = []

	def load(self):
		"""
		Sets up all the tiles that goes with the board.

		Returns
		-------
		None.

		"""
		#Fill with the main tiles
		for x in range(7):
			l = []
			for y in range(7):
				t = Tile(TestData(), self)
				t.move(x*70 +70, y*70 +70)
				l.append(t)
			self.tiles.append(l)

		#Add the input tiles
		for i in range(7):
			if i%2 == 1:
				l = InputTile(TestData(1), self)
				r = InputTile(TestData(3), self)
				l.move(0, i*70 +70)
				r.move(560, i*70 +70)
				self.input_tiles.append(l)
				self.input_tiles.append(r)
		for i in range(7):
			if i%2 == 1:
				u = InputTile(TestData(2), self)
				d = InputTile(TestData(), self)
				u.move(i*70 +70, 0)
				d.move(i*70 +70, 560)
				self.input_tiles.append(u)
				self.input_tiles.append(d)

		#Add the draggable tile
		t = Tile(TestData(), self)
		t.setMovable(True)
		t.move(50, 50)

	def setTilesData(self, dl):
		i = 0
		for l in self.tiles:
			for t in l:
				t.setInternalData(dl[i])
				i+=1

	def resizeEvent(self, event):
		"""
		Used to handle resize events and layout the board.

		Parameters
		----------
		event : QResizeEvent
			The input event.

		Returns
		-------
		None.

		"""
		w = (event.size().width() - 630)/2
		h = (event.size().height() - 630)/2

		#Move all tiles according to the new size.
		for x in range(7):
			for y in range(7):
				self.tiles[x][y].move(x*70+70+w, y*70+70+h)

		for i in range(7):
			if i%2 == 1:
				l = self.input_tiles[i-1]
				r = self.input_tiles[i]
				l.move(w, i*70 +70+h)
				r.move(560+w, i*70 +70+h)
		for i in range(7):
			if i%2 == 1:
				u = self.input_tiles[i-1+6]
				d = self.input_tiles[i+6]
				u.move(i*70 +70+w, h)
				d.move(i*70 +70+w, 560+h)

		super(Board, self).resizeEvent(event)