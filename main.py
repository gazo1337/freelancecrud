from PyQt6.QtWidgets import QApplication
import sys
from main_window import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

app.exec()
