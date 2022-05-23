from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from nothings import TestData

def ensureRaised(w):
	"""
	Ensures that the widget is at the top.

	Parameters
	----------
	w: QWidget
		Widget meant to be raised.
	"""
	#Ensures this draggable is the one at the top-front, so it is no hidden when dragged. Max tiles is 9, plus the congrats popup, so do it 9-1 times.
	for i in range(9):
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
	w: QWidget
		The widget found or None

	"""
	for w in p.parentWidget().children():
		if (w.x() <= pos.x() and w.x()+w.width() >= pos.x()) and (w.y() <= pos.y() and w.y()+w.height() >= pos.y()) and w != p:
			return w
	return None

class Tile(QLabel):
	"""
	UI widget used as a tile.
	"""

	colors = [QColor("#fff"), QColor("#00fdc1"), QColor("#000"), QColor("#7f84ff")]

	def __init__(self, d, parent = None):
		super(Tile, self).__init__(parent)
		self.setFixedSize(70, 70)
		self.setFrameStyle(QFrame.Box | QFrame.Raised)
		self.setLineWidth(1)
		self.setMidLineWidth(3)
		self.setMouseTracking(True)

		self.movable = False
		self.press = False
		self.diff = (0, 0)
		self.source = QPointF(0, 0)
		self._id = -1
		self._data = None
		self.o_target = None
		self._glowing = False
		self._has_moved = False

		self.setInternalData(d)

		self._acceptsMoves = True
		self._pixmap = QPixmap()

	def hasMoved(self):
		return not self._has_moved

	def reset(self):
		self._has_moved = False

	def tileEvent(self, is_in):
		"""
		Not implemented. Reimplement it to receive mouse enter/leave signals when a movable tile hovers this one.

		Parameters
		----------
		is_in: bool
			Wether it is entering (True) or leaving (False) the tile.
		"""
		pass

	def tileRelease(self, tile):
		"""
		Not implemented. Reimplement it to know when a tile is dropped on the tile.

		Parameters
		----------
		tile: Tile
			The other tile dropped on this one.
		"""
		pass

	def setInternalData(self, d):
		"""
		Set the internal data of the tile.

		Parameters
		----------
		d: Unknown.
			The data holder.

		"""
		self._data = d
		if d.pixmap.isNull():
			if not isinstance(d, TestData):
				print("Tile", d.getId(), "has not pixmap!")
			self._pixmap = d.pixmap
		else:
			self._pixmap = d.pixmap.transformed(QTransform().rotate((0 if d.orientation == 0 else (90 if d.orientation == 1 else (180 if d.orientation == 2 else 270)))))
		self.repaint()

	def internalData(self):
		"""
		Get the internal data of the tile.
		"""
		return self._data

	def setMovable(self, mv):
		"""
		Change the ability of the tile to be moved.

		Parameters
		----------
		mv: bool
			Enable the hold tile behaviour on True
		"""
		if not self._acceptsMoves:
			return
		self.movable = mv
		self.press = False
		self.move(self.source.x(), self.source.y())

	def setGlowing(self, enable):
		self._glowing = enable
		self.repaint()

	def mouseMoveEvent(self, event):
		"""
		Handle mouse move events properly to get a drag behaviour.

		Parameters
		----------
		event: QMouseMoveEvent
			The input event.
		"""
		if self.press and self.movable and self.isEnabled():
			#Track to move
			upd = self.mapToParent(event.pos())
			final = QPoint(upd.x() - self.diff[0], upd.y() - self.diff[1])
			self.move(final)
			#If there was a previous target, notify it that we're leaving it.
			if self.o_target:
				self.o_target.tileEvent(False)
			#Dispatch the notification to tell that the tile behind have been entered.
			tmp = widgetAt(self, upd)
			self._has_moved = True
			if isinstance(tmp, InputTile):
				self.o_target = tmp
				if self.o_target != None and isinstance(self.o_target, InputTile):
					self.o_target.tileEvent(True)
					return
		return super(Tile, self).mouseMoveEvent(event)

	def moveEvent(self, event):
		"""
		Handle tile's move in an approriate way.

		Parameters
		----------
		event: QMoveEvent
			The input event.
		"""
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
		"""
		Handle mouse press events and change tile's behaviour depending on it.

		Parameters
		----------
		event: QMouseEvent
			The input event.
		"""
		if self.isEnabled() and self.movable:
			ensureRaised(self) #Shows the widget at top
			self.press = True
			self.source = self.pos()
			upd = self.mapToParent(event.pos())
			self.diff = (upd.x() - self.pos().x(), upd.y() - self.pos().y())
		return super(Tile, self).mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		"""
		Handles release event to get the right drag behaviour.

		Parameters
		----------
		event: QMouseReleaseEvent
			The input event.
		"""
		if self.press and self.movable:
			self.move(self.mapToParent(QPoint(event.pos().x() - self.diff[0], event.pos().y() - self.diff[1])))
			self.press = False
			upd = self.mapToParent(event.pos())
			#If there's a tile under, make it handle the release tile.
			w = widgetAt(self, upd)
			if w and isinstance(w, InputTile):
				w.tileRelease(self)
			return super(Tile, self).mouseReleaseEvent(event)

	def paintEvent(self, event):
		"""
		Handles painting of the widget.

		Parameters
		----------
		event: QPaintEvent
			The input event.
		"""
		p = QPainter(self)
		clipper = QPainterPath()
		clipper.addRoundedRect(QRectF(3, 3, self.width() - 3, self.height() - 3), 5, 5)
		p.setRenderHint(QPainter.Antialiasing)
		p.setClipPath(clipper)

		#Draw the pixmap
		if self._pixmap.isNull():
			p.fillRect(event.rect(), QBrush(QColor(100, 200, 200, 250)))
		else:
			p.drawPixmap(event.rect(), self._pixmap.scaled(self.width(), self.height()), event.rect())

		#Paint the spawn
		if self._data.getSpawn() != 0:
			p.setBrush(QBrush(self._data.spawnColors[self._data.getSpawn()-1]))
			p.setPen(QPen(Qt.gray, 2))
			p.drawEllipse(QRect(20, 20, 30, 30))

		#The glowing effect if needed
		if self._glowing:
			p.fillRect(event.rect(), QBrush(QColor(200, 0, 0, 100)))

		#Add the personas
		i = 0
		while i < len(self._data.getPlayer()):
			x = i//2 *20 + 10
			y = i%2 *20 + 10
			#Paint the dot
			dot = QPainterPath()
			dot.addEllipse(QRectF(x, y, 10, 10))
			p.setPen(QPen(Qt.gray, 2))
			p.drawPath(dot)
			p.fillPath(dot, QBrush(self.colors[self._data.getPlayer()[i]-1]))
			i+=1

		#Paint the border
		p.setBrush(Qt.transparent)
		p.setPen(QPen(Qt.gray, 3))
		p.drawPath(clipper)

#Generate the list of poligons used for the input tiles.
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
	"""
	Get polygons used as arrows (left, right, up and down).

	Returns
	-------
	arrows: list
		List of QPolygon.

	"""
	global arrows
	return arrows

class InputTile(Tile):
	"""
	Tile used to drop another one on it.
	"""
	def __init__(self, d, parent = None):
		super(InputTile, self).__init__(d, parent)
		self.tile_hovered = False
		path = QPainterPath()
		path.addPolygon(get_arrows()[d.orientation])
		self._path = path

	def tileEvent(self, is_in):
		"""
		Handles tile hovers by another one.

		Parameters
		----------
		is_in: bool
			True if the tile enters, False if going out.
		"""
		if is_in and not self.tile_hovered:
			self.tile_hovered = True
			self.repaint()
		elif not is_in and self.tile_hovered:
			self.tile_hovered = False
			self.repaint()

	def tileRelease(self, tile):
		#Clear colors
		self.parentWidget().tileInsertion(self, tile)
		self.tile_hovered = False
		self.repaint()

	def paintEvent(self, ev):
		"""
		Painting handler.

		Parameters
		----------
		ev: QPaintEvent
			The input event.
		"""
		clipper = QPainterPath()
		clipper.addRoundedRect(QRectF(3, 3, self.width() - 3, self.height() - 3), 5, 5)

		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setClipPath(clipper)

		if self.tile_hovered:
			painter.fillRect(self.rect(), QBrush(Qt.green))
		else:
			painter.fillRect(self.rect(), QBrush(Qt.gray))
		painter.fillPath(self._path, QBrush(Qt.yellow))
		painter.end()
		#return super(InputTile, self).paintEvent(ev)
