from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

def ensureRaised(w):
	"""
	Ensures that the widget is at the top.

	Parameters
	----------
	w : QWidget
		Widget meant to be raised.

	Returns
	-------
	None.

	"""
	#Ensures this draggable is the one at the top-front, so it is no hidden when dragged. Max tiles is 9, plus the congrats popup, so do it 9-1 times.
	for i in range(9):
		w.raise_()

def widgetAt(p, pos):
	"""
	Get the widget at a position.

	Parameters
	----------
	p : QWidget
		A widget to escape.
	pos : QPoint
		Target point.

	Returns
	-------
	w : TYPE
		DESCRIPTION.

	"""
	for w in p.parentWidget().children():
		if (w.x() <= pos.x() and w.x()+w.width() >= pos.x()) and (w.y() <= pos.y() and w.y()+w.height() >= pos.y()) and w != p:
			return w
	return None

class Tile(QLabel):
	def __init__(self, d, parent = None):
		super(Tile, self).__init__(parent)
		self.setFixedSize(70, 70)
		self.setFrameStyle(QFrame.Box | QFrame.Raised)
		self.setLineWidth(1)
		self.setMidLineWidth(3)
		self.setMouseTracking(True)
		self.setInternalData(d)

		self.movable = False
		self.press = False
		self.diff = (0, 0)
		self.source = QPointF(0, 0)
		self._id = -1
		self._data = None
		self.o_target = None

	def tileEvent(self, is_in):
		"""
		Not implemented. Reimplement it to receive mouse enter/leave signals when a movable tile hovers this one.

		Parameters
		----------
		is_in : bool
			DESCRIPTION.

		Returns
		-------
		None.

		"""
		pass

	def setInternalData(self, d):
		"""
		Set the internal data of the tile.

		Parameters
		----------
		d : Unknown.
			The data holder.

		"""
		self._data = d
		if not d.pixmap.isNull():
			self.setPixmap(d.pixmap.scaled(self.width(), self.height()))
		else:
			self.pixmap = d.pixmap
		self.update()

	def setMovable(self, mv):
		"""
		Change the ability of the tile to be moved.

		Parameters
		----------
		mv : bool
			Enable the hold tile behaviour on True

		Returns
		-------
		None.

		"""
		self.movable = mv
		self.press = False
		self.move(self.source.x(), self.source.y())

	def mouseMoveEvent(self, event):
		"""
		Handle mouse move events properly to get a drag behaviour.

		Parameters
		----------
		event : QMouseMoveEvent
			The input event.

		Returns
		-------
		None.

		"""
		if self.press and self.movable:
			#Track to move
			upd = self.mapToParent(event.pos())
			final = QPoint(upd.x() - self.diff[0], upd.y() - self.diff[1])
			self.move(final)
			#If there was a previous target, notify it that we're leaving it.
			if self.o_target:
				self.o_target.tileEvent(False)
			#Dispatch the notification to tell that the tile behind have been entered.
			self.o_target = widgetAt(self, upd)
			if self.o_target != None and isinstance(self.o_target, InputTile):
				self.o_target.tileEvent(True)
				return
		return super(Tile, self).mouseMoveEvent(event)

	def moveEvent(self, event):
		"""
		Handle tile's move in an approriate way.

		Parameters
		----------
		event : QMoveEvent
			The input event.

		Returns
		-------
		None.

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
		event : QMouseEvent
			The input event.

		Returns
		-------
		None.

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
		event : QmouseReleaseEvent
			The input event.

		Returns
		-------
		None.

		"""
		if self.press and self.movable:
			self.press = False
			upd = self.mapToParent(event.pos())
			return super(Tile, self).mouseReleaseEvent(event)

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
	arrows : list
		List of QPolygon.

	"""
	global arrows
	return arrows

class InputTile(Tile):
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
		is_in : bool
			True if the tile enters, False if going out.

		Returns
		-------
		None.

		"""
		if is_in and not self.tile_hovered:
			self.tile_hovered = True
			self.repaint()
		elif not is_in and self.tile_hovered:
			self.tile_hovered = False
			self.repaint()

	def paintEvent(self, ev):
		"""
		Painting handler.

		Parameters
		----------
		ev : QPaintEvent
			The input event.

		Returns
		-------
		None.

		"""
		painter = QPainter()
		painter.begin(self)
		if self.tile_hovered:
			painter.fillRect(self.rect(), QBrush(Qt.green))
		painter.fillPath(self._path, QBrush(Qt.yellow))
		painter.end()
		return super(InputTile, self).paintEvent(ev)
