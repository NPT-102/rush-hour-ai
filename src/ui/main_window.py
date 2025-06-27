from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
import sys

from strategy_selector import StrategySelector

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("test")
        self.setMinimumSize(400, 200)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.strategy_selector = StrategySelector()
        layout.addWidget(self.strategy_selector, alignment=Qt.AlignCenter)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
