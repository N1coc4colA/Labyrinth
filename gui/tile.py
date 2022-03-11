from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

def ensureRaised(w):
	#Ensures this draggable is the one at the top-front, so it is no hidden when dragged. Max tiles is 9, plus the congrats popup, so do it 9-1 times.
	for i in range(9):
		w.raise_()

def widgetAt(p, pos):
	for w in p.parentWidget().children():
		if (p.x() <= pos.x() and p.x()+p.width() >= pos.x()) and (p.y() <= pos.y() and p.y()+p.height() >= pos.y()) and w != p:
			return p

class Tile(QLabel):
	def __init__(self, d, parent = None):
		super(Tile, self).__init__(parent)
		self.setFixedSize(70, 70)
		self.setFrameStyle(QFrame.Box | QFrame.Raised)
		self.setLineWidth(1)
		self.setMidLineWidth(3)
		self.setMouseTracking(True)
		self.setText("A")

		self.movable = False
		self.press = False
		self.diff = (0, 0)
		self.source = QPointF(0, 0)
		self._id = -1
		self._data = d

	def internalData(self, d):
		self._data = d
		self.update()

	def setMovable(self, mv):
		self.movable = mv
		self.press = False
		self.move(self.source.x(), self.source.y())

	def mouseMoveEvent(self, event):
		if self.press and self.movable:
			#Track to move
			upd = self.mapToParent(event.pos())
			final = QPoint(upd.x() - self.diff[0], upd.y() - self.diff[1])
			self.move(final)
		return super(Tile, self).mouseMoveEvent(event)

	def moveEvent(self, event):
		if not self.press:
			#Update when the move is a 'normal' one, used while changing game board with anims mainly.
			self.source = self.mapToParent(self.pos())
			return super(Tile, self).moveEvent(event)
		else:
			w = widgetAt(self, self.source)
			if w and isinstance(w, InputTile):
				w.tile_hovered = True
				w.repaint()

	def mousePressEvent(self, event):
		if self.isEnabled() and self.movable:
			ensureRaised(self) #Shows the widget at top
			self.press = True
			self.source = self.pos()
			upd = self.mapToParent(event.pos())
			self.diff = (upd.x() - self.pos().x(), upd.y() - self.pos().y())
		return super(Tile, self).mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		if self.press and self.movable:
			self.press = False
			upd = self.mapToParent(event.pos())
			return super(Tile, self).mouseReleaseEvent(event)

arrows = {}
p = QPolygonF()
p << QPointF(35, 10) << QPointF(10, 60) << QPointF(60, 60)
arrows[0] = p
p = QPolygonF()
p << QPointF(60, 35) << QPointF(10, 10) << QPointF(10, 60)
arrows[1] = p
p = QPolygonF()
p << QPoint(35, 60) << QPointF(10, 10) << QPointF(60, 10)
arrows[2] = p
p = QPolygonF()
p << QPointF(10, 35) << QPointF(60, 10) << QPointF(60, 60)
arrows[3] = p

def get_arrows():
	global arrows
	return arrows

class InputTile(Tile):
	def __init__(self, d, parent = None):
		super(InputTile, self).__init__(d, parent)
		self.tile_hovered = False
		self.setText("B")
		path = QPainterPath()
		path.addPolygon(get_arrows()[d.orientation])
		self._path = path

	def mouseMoveEvent(self, event):
		#Get the upper tile
		upd = self.mapToParent(event.pos())
		if (self.x() <= upd.x() and self.x()+self.width() >= upd.x()) and (self.y() <= upd.y() and self.y()+self.height() >= upd.y()):
			if not self.tile_hovered:
				self.tile_hovered = True
				self.repaint()
			else:
				self.tile_hovered = False
				self.repaint()
		elif self.tile_hovered:
			self.tile_hovered = False
			self.repaint()
		return super(InputTile, self).mouseMoveEvent(event)

	def paintEvent(self, ev):
		painter = QPainter()
		painter.begin(self)
		if self.tile_hovered:
			painter.fillRect(self.rect(), QBrush(Qt.green))
		painter.fillPath(self._path, QBrush(Qt.yellow))
		painter.end()
		return super(InputTile, self).paintEvent(ev)

