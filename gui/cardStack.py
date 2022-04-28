#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class CardStack(QWidget):
	def __init__(self, parent = None):
		super(CardStack, self).__init__(parent)
		self._stack = None
		self.setFixedSize(100, 200)

	def setStack(self, s):
		self._stack = s
		self.update()

	def stack(self):
		return self._stack

	def paintEvent(self, ev):
		path = QPainterPath()
		path.addRoundedRect(QRectF(0, 0, 100, 200))
		p = QPainter(self)
		p.setClipPath(path)
		d = 50/len(self._stack)
		l = len(self._stack)

		if l == 0:
			empty = QPainterPath()
			empty.addRoundedRect(0, 50, 100, 150, 10, 10)
			p.fillPath(empty, QBrush(QColor(200, 200, 200)))
		else:
			i = 1
			while i < l:
				y = 200-(d*i)-1
				img = QPainterPaht()
				img.addRoundedRect(QRectF(0, y, d*i+1), 10, 10)
				p.fillPath(img, QBrush(Qt.gray))
				p.setPen(QPen(Qt.black, 3))
				p.drawPath(img)
				i+=1

		img = QPainterPath()
		img.addRounded(QRectF(0, 0, 100, 150), 10, 10)
		p.fillPath(img, QBrush(Qt.gray)) #The card's BG
		brush = QBrush(self._stack.top().pixmap()) #Build with the input pixmap
		p.fillPath(img, brush)
		p.setPen(QPen(Qt.black, 3))
		p.drawPath(img)