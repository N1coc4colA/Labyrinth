#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class CardStack(QWidget):
	def __init__(self, parent = None):
		super(CardStack, self).__init__(parent)
		self._stack = []
		self.setFixedSize(100, 200)

	def setStack(self, s):
		self._stack = s

	def stack(self):
		return self._stack

	def paintEvent(self, ev):
		path = QPainterPath()
		path.addRoundedRect(QRectF(0, 0, 100, 200))
		p = QPainter(self)
		p.setClipPath(path)
		d = 50/len(self._stack)
		l = len(i)

		if l == 0:
			return
		else:
			i = 1
			while i < l:
				img = QPainterPaht()
				img.addRoundedRect(QRectF(), 10, 10)
				brush = QBrush() #Build with the input pixmapp
				p.fillPath(img, Qt.gray)
				p.setPen(QPen(Qt.black, 3))
				p.drawPath(img)
				i+=1

		img = QPainterPath()
		img.addRounded(QRectF(0, 0, 100, 150), 10, 10)
		p.fillPath(img, QBrush(Qt.gray))
		brush = QBrush() #Build with the input pixmap
		p.fillPath(img, brush)
		p.setPen(Qt.black, 3))
		p.drawPath(img)