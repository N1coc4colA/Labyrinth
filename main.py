from PyQt5.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)

from gui.gameboard import Board
from data.laby_info import BoardBackend

bkd = BoardBackend(2)
b = Board()
b.load()
b.show()
b.setBackend(bkd)
sys.exit(app.exec())
