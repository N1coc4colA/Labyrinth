from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from gui.tile import Tile, InputTile
from gui.rotationController import RotationController

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
		self.setMinimumSize(730, 730)
		self.tiles = []
		self.input_tiles = []
		self.running_animations = []
		self.currentlyUsed = None

		self.backend = None
		self.controller = RotationController(self)
		self.controller.setFixedSize(150, 50)
		self.controller.valueChanged.connect(self.rotateTile)

		self._timer = QTimer()
		self._timer.setInterval(750)
		self._timer.setSingleShot(True)
		self._timer.timeout.connect(self.unlock)

	def unlock(self):
		ensureRaised(self.currentlyUsed)
		self.layoutTable(self.size()) #Needed as sometimes, tiles' position fails (SAD)
		self.setEnabled(True)

	def lockForAnims(self):
		self._timer.stop()
		self._timer.start()

	def setBackend(self, bkd):
		self.backend = bkd
		self.setTilesData(bkd.board)
		self.currentlyUsed.setInternalData(bkd.current)

	def forceUpdate(self):
		for l in self.tiles:
			for t in l:
				t.update()
		self.currentlyUsed.update()

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

	def layoutTable(self, size):
		w = (size.width() - 630)/2
		h = (size.height() - 630)/2

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

	def resizeEvent(self, event):
		"""
		Used to handle resize events and layout the board.

		Parameters
		----------
		event: QResizeEvent
			The input event.
		"""
		self.layoutTable(event.size())
		#Move the controller
		self.controller.move(event.size().width() - 5 - self.controller.width(), event.size().height() - 5 - self.controller.height())

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
			return t
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

	def rotateTile(self, val):
		"""
		Rotate the current tile of the given angle.

		Parameters
		----------
		val: int
			The angle identifier.
		"""
		#[TODO] Implement it
		pass

	def rowOf(self, tile):
		for x in range(7):
			for y in range(7):
				if self.tiles[x][y] == tile:
					return x
		return -1

	def columnOf(self, tile):
		for x in range(7):
			for y in range(7):
				if self.tiles[x][y] == tile:
					return y
		return -1

	def tileInsertion(self, source, target):
		self.removeGlowing()

		#Tell the backend that we're moving
		self.running_animations.clear();
		self.forceUpdate()

		w = (self.width() - 630)/2
		h = (self.height() - 630)/2
		#Check direction
		p = source.pos()
		horizontal = False
		beg = False
		fin = target.pos()
		if w <= p.x() and p.x() <= w+70:
			horizontal = True
			beg = True
		elif 70*8+w <= p.x() and p.x() <= 70*9+w:
			horizontal = True
		elif not horizontal and h <= p.y() and p.y() <= h+70:
			beg = True

		#Generate animations and lock UI.
		self.setEnabled(False)
		target.setMovable(False)

		if beg:
			#First of all update all the table.
			v = (self.columnOf(self.tileAt(QPoint(w+140, p.y()+1))) if horizontal else self.rowOf(self.tileAt(QPoint(p.x()+1, h+140)))) #We can use a random tile, no need to make it more complex.
			edge = self.tiles[(6 if horizontal else v)][(v if horizontal else 6)]

			i = 6
			while i > -1:
				self.tiles[(i if horizontal else v)][(v if horizontal else i)] = (self.currentlyUsed if (i == 0) else self.tiles[(i-1 if horizontal else v)][(v if horizontal else i-1)])
				i -= 1
			self.currentlyUsed = edge

			#Generate the animations
			c = QPropertyAnimation(target, b"pos")
			c.setStartValue(target.pos())
			c.setEndValue(QPoint((p.x()+70 if horizontal else p.x()+1), (p.y()+1 if horizontal else p.y()+70)))
			c.setDuration(700)
			c.setEasingCurve(QEasingCurve.InOutCubic)

			i = 1
			while i < 8:
				pos = QPoint((w+i*70+70 if horizontal else p.x()+1), (p.y()+1 if horizontal else h+i*70+70))
				a = QPropertyAnimation(self.tileAt(pos), b"pos")
				a.setEndValue(QPoint((pos.x()+70 if horizontal else pos.x()), (pos.y() if horizontal else pos.y()+70)))
				a.setDuration(700)
				a.setEasingCurve(QEasingCurve.InOutCubic)
				self.running_animations.append(a)
				i += 1

			objective = QPoint((w+i*70 if horizontal else p.x()+1), (p.y()+1 if horizontal else h+i*70))
			result = self.tileAt(objective)

			b = QPropertyAnimation(result, b"pos")
			b.setStartValue(QPoint((objective.x()-70 if horizontal else objective.x()), (objective.y() if horizontal else objective.y()-70)))
			b.setEndValue(fin)
			b.setDuration(700)
			b.setEasingCurve(QEasingCurve.InOutCubic)

			#Make sure the new tile can be moved by the user.
			result.setMovable(True)

			#Run the animations
			self.running_animations.append(b)
			self.running_animations.append(c)
			for anim in self.running_animations:
				anim.start()
		else:
			#First of all update all the table.
			v = (self.columnOf(self.tileAt(QPoint(w+140, p.y()+1))) if horizontal else self.rowOf(self.tileAt(QPoint(p.x()+1, h+140))))#We can use a random tile, no need to make it more complex.
			edge = self.tiles[(0 if horizontal else v)][(v if horizontal else 0)]

			i = 0
			while i < 7:
				self.tiles[(i if horizontal else v)][(v if horizontal else i)] = (self.currentlyUsed if (i == 6) else self.tiles[(i+1 if horizontal else v)][(v if horizontal else i+1)])
				i += 1
			self.currentlyUsed = edge

			#Generate the animations
			c = QPropertyAnimation(target, b"pos")
			c.setStartValue(target.pos())
			c.setEndValue(QPoint((p.x()-70 if horizontal else p.x()+1), (p.y()+1 if horizontal else p.y()-70)))
			c.setDuration(700)
			c.setEasingCurve(QEasingCurve.InOutCubic)

			i = 2
			while i < 8:
				pos = QPoint((w+i*70+70 if horizontal else p.x()+1), (p.y()+1 if horizontal else h+i*70+70))
				a = QPropertyAnimation(self.tileAt(pos), b"pos")
				a.setEndValue(QPoint((pos.x()-140 if horizontal else pos.x()), (pos.y() if horizontal else pos.y()-140)))
				a.setDuration(700)
				a.setEasingCurve(QEasingCurve.InOutCubic)
				self.running_animations.append(a)
				i += 1

			objective = QPoint((w+140 if horizontal else p.x()+1), (p.y()+1 if horizontal else h+140))
			result = self.tileAt(objective)

			b = QPropertyAnimation(result, b"pos")
			b.setStartValue(QPoint((objective.x()+70 if horizontal else objective.x()), (objective.y() if horizontal else objective.y()+70)))
			b.setEndValue(target.pos())
			b.setDuration(700)
			b.setEasingCurve(QEasingCurve.InOutCubic)

			#Make sure the new tile can be moved by the user.
			result.setMovable(True)

			#Run the animations
			#self.running_animations.append(b)
			self.running_animations.append(c)
			for anim in self.running_animations:
				anim.start()

		#Push update to BKD
		self.lockForAnims()