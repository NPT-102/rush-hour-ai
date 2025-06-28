from PySide6.QtWidgets import QComboBox, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Signal, Qt

class MapSelector(QWidget):
    map_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.difficulties = []
        self.comboBox = QComboBox()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.currentMap = 0

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)

        self.comboBox.currentIndexChanged.connect(self.handle_map_change)

    def get_current_map(self):
        return self.currentMap
    
    def insert_map(self, difficulty):
        self.difficulties.append(difficulty)
        self.comboBox.addItem(f"Map {len(self.difficulties)}")
        if len(self.difficulties) == 1:
            self.label.setText(difficulty)

    def handle_map_change(self, index):
        self.currentMap = index
        print(self.currentMap)
        difficulty = self.difficulties[index]
        self.label.setText(difficulty)
        self.map_changed.emit(index)