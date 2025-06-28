from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
import sys

from strategy_selector import StrategySelector
from map_selector import MapSelector
from stats_board import StatsBoard

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("test")
        self.setMinimumSize(400, 200)

        central_widget = QWidget()
        layout = QVBoxLayout()

        # self.strategy_selector = StrategySelector()
        self.map_selector = MapSelector()
        # layout.addWidget(self.strategy_selector, alignment=Qt.AlignCenter)
        layout.addWidget(self.map_selector, alignment=Qt.AlignCenter)
        self.stats = StatsBoard()
        layout.addWidget(self.stats, alignment=Qt.AlignCenter)
        self.stats.update_stats(2, 100)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
