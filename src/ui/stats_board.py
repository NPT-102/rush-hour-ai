from PySide6.QtWidgets import QGridLayout, QWidget, QLabel
from PySide6.QtCore import Qt, Signal


class StatsBoard(QWidget):
    stats_updated = Signal((int, int))
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.labels = [QLabel("Step count:"), QLabel("0"),
                       QLabel("Total cost:"), QLabel("0")]
        layout = QGridLayout()
        for i in range(len(self.labels)):
            layout.addWidget(self.labels[i], i // 2, i % 2)
            if i % 2 == 0:
                self.labels[i].setAlignment(Qt.AlignRight)
            else:
                self.labels[i].setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

    def update_stats(self, step_count, total_cost):
        self.labels[1].setText(str(step_count))
        self.labels[3].setText(str(total_cost))