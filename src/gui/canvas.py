import tkinter as tk
from grid import Grid

# the screen showing the game board
# implement later when i understand the game logic :)
class Canvas(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.create_widget()
        

    def create_widget(self):
        self.grid = Grid(self)

    def on_state_change(self, state):
        pass