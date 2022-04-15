from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import time

from gui.tile import Tile, InputTile
def ensureRaised(w):
	"""
	Ensures that the widget is at the top.

	Parameters
	----------
	w: QWidget
		Widget meant to be raised.
	"""
	#Ensures this draggable is the one at the top-front, so it is no hidden when dragged. Max tiles is 9, plus the congrats popup, so do it 9-1 times.
	for i in range(65):
		w.raise_()

def widgetAt(p, pos):
	"""
	Get the widget at a position.

	Parameters
	----------
	p: QWidget
		A widget to escape.
	pos: QPoint
		Target point.

	Returns
	-------
	w: TYPE
		DESCRIPTION.

	"""
	for w in p.children():
		if (w.x() <= pos.x() and w.x()+w.width() >= pos.x()) and (w.y() <= pos.y() and w.y()+w.height() >= pos.y()) and w != p:
			return w
	return None

def smartRaiseUp(p, pos):
	pass

class TestData:
	def __init__(self, o = 0):
		self.orientation = o
		self.pixmap = QPixmap()

	def getId(self):
		return 0

class Board(QWidget):
	def __init__(self, parent = None):
		super(Board, self).__init__(parent)
		self.setMinimumSize(630, 630)
		self.tiles = []
		self.input_tiles = []
		self.backend = None
		self.running_animations = []
		self.currentlyUsed = None
		self._timer = QTimer()
		self._timer.setInterval(700)
		self._timer.setSingleShot(True)
		self._timer.timeout.connect(self.unlock)

	def unlock(self):
		self.setEnabled(True)

	def lockForAnims(self):
		self._timer.stop()
		self._timer.start()

	def setBackend(self, bkd):
		self.backend = bkd
		self.setTilesData(bkd.board)
		self.currentlyUsed.setInternalData(bkd.current)

	def load(self):
		"""
		Sets up all the tiles that goes with the board.
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
		self.currentlyUsed = t

	def setTilesData(self, dl):
		for i in range(7):
			for j in range(7):
				self.tiles[i][j].setInternalData(dl[i][j])

	def resizeEvent(self, event):
		"""
		Used to handle resize events and layout the board.

		Parameters
		----------
		event: QResizeEvent
			The input event.
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

	def tileAt(self, pos, p = None):
		"""
		Get the widget at a position.

		Parameters
		----------
		p: gui.tile.Tile
			A tile to escape.
		pos: QPoint
			The target point.

		Returns
		-------
		w: gui.tile.Tile or None
			The tile found

		"""
		t = self.currentlyUsed
		if t != None and (t.x() <= pos.x() and t.x()+t.width() >= pos.x()) and (t.y() <= pos.y() and t.y()+t.height() >= pos.y()) and t != p:
			return w
		for l in self.tiles:
			for w in l:
				if (w.x() <= pos.x() and w.x()+w.width() >= pos.x()) and (w.y() <= pos.y() and w.y()+w.height() >= pos.y()) and w != p:
					return w
		return None

	def removeGlowing(self):
		"""
		Stops the glowing effect of all the tiles.

		"""
		l = self.children()
		for w in l:
			if isinstance(w, Tile):
				w.setGlowing(False)

	def swapTile(self, begin):
		#[TODO] Fix that list mess
		for x in range(7):
			for y in range(7):
				if self.tiles[x][y] == begin:
					print("Found the result at", x, y, "val:", self.tiles[x][y])
					self.tiles[x][y] = self.currentlyUsed
		self.currentlyUsed = begin
		print("val:", self.currentlyUsed)

	def tileInsertion(self, source, target):
		#Tell the backend that we're moving
		self.running_animations.clear();

		w = (self.width() - 630)/2
		h = (self.height() - 630)/2
		#Check direction
		p = source.pos()
		horizontal = False
		beg = False
		fin = target.pos()
		if p.x() == w:
			horizontal = True
			beg = True
		if p.x() == 70*7+w:
			horizontal = True
		if not horizontal and p.y() == h:
			beg = True

		#Generate animations and lock UI.
		self.setEnabled(False)
		target.setMovable(False)

		#Stack the moved tiles under the movable one.
		if horizontal:
			target.setGlowing(True)
			c = QPropertyAnimation(target, b"pos")
			c.setStartValue(target.pos())
			if (beg):
				c.setEndValue(QPoint(p.x()+70, p.y()+1))
			else:
				c.setEndValue(QPoint(p.x()-70, p.y())+1)
			c.setDuration(700)
			c.setEasingCurve(QEasingCurve.InOutCubic)

			i = 1
			while i < 8:
				t_x = w+i*70+70
				end_pos = QPoint(t_x, p.y()+1)
				start_pos = QPoint(t_x, p.y()+1)
				tile = self.tileAt(start_pos)

				a = QPropertyAnimation(tile, b"pos")
				a.setEndValue(end_pos)
				a.setDuration(700)
				a.setEasingCurve(QEasingCurve.InOutCubic)
				self.running_animations.append(a)

				i += (1 if beg else -1)

			objective = QPoint(w+i*70, p.y()+1)
			result = self.tileAt(objective)
			result.setMovable(True)
			ensureRaised(result)

			b = QPropertyAnimation(result, b"pos")
			b.setStartValue(QPoint(objective.x() + (-70 if beg else 0), objective.y()))
			b.setEndValue(fin)
			b.setDuration(700)
			b.setEasingCurve(QEasingCurve.InOutCubic)
			self.running_animations.append(b)
			self.running_animations.append(c)

			#Exchange the current tile with the end one.
			self.swapTile(result)

			for anim in self.running_animations:
				anim.start()

			#Push update to BKD
		else:
			for i in range(0,6):
				a = QPropertyAnimation(widgetAt(self, QPoint(p.x(), w+i*70)), b"pos")
				a.setEndValue(pb)
				a.setDuration(750)
				a.setEasingCurve(QEasingCurve.InOutCubic)
				self.running_animations.append(a)
				a.start()
		self.removeGlowing()
		self.lockForAnims()