from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel
)
from PySide6.QtCore import Qt, Signal
import sys
from main_window import MainWindow
from strategy_selector import StrategySelector

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())