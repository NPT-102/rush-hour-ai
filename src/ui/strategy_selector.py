from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal

class StrategySelector(QWidget):
    strategy_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.left_button = QPushButton("<")
        self.right_button = QPushButton(">")
        self.label = QLabel("hi there")
        layout = QHBoxLayout()
        layout.addWidget(self.left_button)
        layout.addWidget(self.label)
        layout.addWidget(self.right_button)
        self.setLayout(layout)