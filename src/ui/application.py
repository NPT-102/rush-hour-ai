from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget

import sys

app = QApplication(sys.argv)

window  = QMainWindow()
window.setWindowTitle("Rush Hour")



button = QPushButton("hey")
button2 = QPushButton("hey")
button3 = QPushButton("wow")

layout = QGridLayout()
layout.addWidget(button, 0, 0)
layout.addWidget(button2, 1, 0)
layout.addWidget(button3, 0, 1, 2, 1)

centralWidget = QWidget()
centralWidget.setLayout(layout)

window.setCentralWidget(centralWidget)

window.show()
app.exec()