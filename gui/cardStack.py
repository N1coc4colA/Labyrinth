from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class CardStack(QWidget):
	"""
	Widget representing the cards of a player.
	"""
	def __init__(self, parent = None):
		super(CardStack, self).__init__(parent)
		self._stack = None
		self.setFixedSize(100, 200)

	def setStack(self, s):
		"""
		Set the internal data of the stack.

		Parameters
		----------
		s : Unknown.
			The data holder.

		Returns
		-------
		None.

		"""
		self._stack = s
		self.update()

	def stack(self):
		return self._stack

	def paintEvent(self, ev):
		path = QPainterPath()
		path.addRoundedRect(QRectF(0, 0, 100, 200), 10, 10)
		p = QPainter(self)
		p.setClipPath(path)
		l = len(self._stack)

		#Make it empty, so the user knows he has no more to look for anything.
		if l == 0:
			empty = QPainterPath()
			empty.addRoundedRect(0, 50, 100, 150, 10, 10)
			p.fillPath(empty, QBrush(QColor(200, 200, 200)))
			pen = QPen(Qt.black, 2)
			pen.setStyle(Qt.DashLine)
			p.setPen(pen)
			p.drawPath(empty)
			return

		#Paint the edges of the card that are not discovered yet.
		d = 50/len(self._stack)
		i = 1
		while i < l:
			y = 200-(d*(i+1))-20
			img = QPainterPath()
			img.addRoundedRect(QRectF(0, y, 100, d*i+20), 10, 10)
			p.fillPath(img, QBrush(Qt.gray))
			p.setPen(QPen(Qt.black, 3))
			p.drawPath(img)
			i+=1

		#Put the uncovered card.
		img = QPainterPath()
		img.addRoundedRect(QRectF(0, 0, 100, 150), 10, 10)
		p.fillPath(img, QBrush(Qt.gray)) #The card's BG
		brush = QBrush(self._stack.top().pixmap().scaled(100, 150, Qt.KeepAspectRatio)) #Build with the input pixmap
		p.fillPath(img, brush)
		p.setPen(QPen(Qt.black, 3))
		p.drawPath(img)