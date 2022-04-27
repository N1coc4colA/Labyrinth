from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

def intersectedInto(a, b):
	if not QRectF(a).intersects(QRectF(b)):
		return QRectF(0, 0, 0, 0)
	out = QRectF(a).intersected(QRectF(b))
	if b.x() < out.x():
		out.setX(0)
	if b.y() < out.y():
		out.setY(0)
	return out

class RotationController(QWidget):
	"""
	Input widget to rotate clockwise using degrees steps.
	"""

	valueChanged = pyqtSignal(int)

	def __init__(self, parent = None):
		super(RotationController, self).__init__(parent)
		self.setMouseTracking(True)

		self._hovers = False
		self._clicks = False
		self._side = 0
		self._itemSize = (0, 0)
		self._icons = (QIcon("./images/rotate-left-solid.svg"), QIcon("./images/rotate-right-solid.svg"))
		self._lowest = self.height()
		self._pixmaps = (self._icons[0].pixmap(QSize(self.height(), self.height())), self._icons[1].pixmap(QSize(self.height(), self.height())))
		self._value = 0
		self._step = 90
		self._convertToSteps = True

	def setConvertToSteps(self, enable):
		self._converToSteps = True

	def doesConvertToSteps(self):
		return self._convertToSteps

	def setStep(self, s):
		self._step = s

	def step(self):
		return self._steps

	def setValue(self, v):
		self._value = v

	def value(self):
		if self._convertToSteps:
			return self._value//self._step
		return self._value

	def change(self, i):
		self._value += i*self._step
		#Automatically make in the 360° range.
		self._value += (360 if (self._value < 0)  else (-360 if (360 <= self._value) else 0))
		self.valueChanged.emit(self.value())

	def pointInside(self, p):
		if (p.y() > 5 and p.y() < (5 + self._itemSize[1])):
			if p.x() > 5 and p.x() < (5 + self._itemSize[0]):
				return 1
			elif  p.x() > (5 + self._itemSize[0]) and (5 + self._itemSize[0]*2):
				return 2
		return 0

	def getSide(self, a, b = None, c = None, d = None):
		if (b == None):
			return self.pointInside(a)
		else:
			check = [self.pointInside(a), self.pointInside(b), self.pointInside(c), self.pointInside(d)]
			if 1 in check and 2 in check:
				return 3
			elif 1 in check:
				return 1
			elif 2 in check:
				return 2
			#Else, all might be outside of both! Meaning that it has to be both too ;)
			if a.x() < 5 and a.y() < 5 and b.x() > (5 + self._itemSize[0]*2) and b.y() < 5 and c.x() < 5 and c.y() > (5 + self._itemSize[1]) and d.x() > (5 + self._itemSize[0]*2) and d.x() > (5 + self._itemSize[1]):
				return 3
		return 0

	def resizeEvent(self, e):
		self._itemSize = ((e.size().width() - 10)/2, e.size().height() - 10)
		lowest = (self._itemSize[0] if self._itemSize[0] < self._itemSize[1] else self._itemSize[1])
		self._pixmaps = (self._icons[0].pixmap(lowest, lowest), self._icons[1].pixmap(lowest, lowest))
		self._lowest = lowest
		super(RotationController, self).resizeEvent(e)

	def leaveEvent(self, e):
		self._hovers = False
		self.repaint()
		super(RotationController, self).leaveEvent(e)

	def enterEvent(self, e):
		self._hovers = True
		self.repaint()
		super(RotationController, self).enterEvent(e)

	def mousePressEvent(self, e):
		super(RotationController, self).mousePressEvent(e)
		self._side = self.getSide(e.pos())
		self._clicks = True
		self.repaint()

	def mouseReleaseEvent(self, e):
		self._clicks = False
		self._side = self.getSide(e.pos())
		if self._side == 1:
			self.change(1)
		elif self._side == 2:
			self.change(-1)
		self.repaint()
		super(RotationController, self).mouseReleaseEvent(e)

	def mouseMoveEvent(self, e):
		self._side = self.getSide(e.pos())
		self.repaint()
		super(RotationController, self).mouseMoveEvent(e)

	def paintPixmapRight(self, e, p):
		p.drawPixmap(QRect(5 + self._itemSize[0] + (self._itemSize[0] - self._lowest)/2, 5 + (self._itemSize[1] - self._lowest)/2, self._lowest, self._lowest), self._pixmaps[1])

	def paintPixmapLeft(self, e, p):
		p.drawPixmap(QRect(5 + (self._itemSize[0] - self._lowest)/2, 5 + (self._itemSize[1] - self._lowest)/2, self._lowest, self._lowest), self._pixmaps[0])

	def paintEvent(self, e):
		p = QPainter()
		p.begin(self)
		clipper = QPainterPath()
		clipper.addRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)
		p.setClipPath(clipper)

		#Basic BG
		p.fillRect(e.rect(), QBrush(Qt.white))
		p.setPen(QPen(QColor(230, 230, 230), 2))
		p.drawPath(clipper)

		if self._side != 0:
			#Put the effects
			path = QPainterPath()
			path.addRoundedRect(QRectF(5, 5, self._itemSize[0] *2, self._itemSize[1]), 5, 5)
			p.setClipPath(path)
			if self._clicks:
				p.fillRect(QRectF(5 + (self._itemSize[0] if (self._side == 2) else 0), 5, self._itemSize[0], self._itemSize[1]), QBrush(self.palette().color(self.palette().currentColorGroup(), QPalette.Highlight)))
			elif self._hovers:
				p.fillRect(QRectF(5 + (self._itemSize[0] if (self._side == 2) else 0), 5, self._itemSize[0], self._itemSize[1]), QBrush(QColor(220, 220, 220)))
		#Draw arrows if needed.
		side = self.getSide(e.rect().topLeft(), e.rect().topRight(), e.rect().bottomLeft(), e.rect().bottomRight())
		if side == 1:
			self.paintPixmapLeft(e, p)
		elif side == 2:
			self.paintPixmapRight(e, p)
		elif side == 3:
			self.paintPixmapLeft(e, p)
			self.paintPixmapRight(e, p)
		p.end()
