from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal

class StrategySelector(QWidget):
    strategy_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.strategies = []
        self.index = 0

        self.left_button = QPushButton("<")
        self.right_button = QPushButton(">")
        self.label = QLabel("Search algo")
        self.label.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        layout.addWidget(self.left_button)
        layout.addWidget(self.label)
        layout.addWidget(self.right_button)
        self.setLayout(layout)
        
        self.left_button.clicked.connect(self.prev_strategy)
        self.right_button.clicked.connect(self.next_strategy)
        
    def prev_strategy(self):
        self.index = (self.index - 1) % len(self.strategies)
        self.handle_strategy_change()
        
    def next_strategy(self):
        self.index = (self.index + 1) % len(self.strategies)
        self.handle_strategy_change()
        
    def handle_strategy_change(self):
        strategy = self.strategies[self.index]
        self.label.setText(strategy)
        self.strategy_changed.emit(strategy)
        
    def get_current_strategy(self):
        return self.strategies[self.index]
    
    def insert_strategy(self, strat):
        self.strategies.append(strat)