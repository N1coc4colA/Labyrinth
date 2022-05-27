from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ResultWidget(QLabel):
	"""
	Shows wether you won or not with an animation.
	"""

	def __init__(self, d, parent = None):
		super(ResultWidget, self).__init__(parent)