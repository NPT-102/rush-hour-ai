import tkinter as tk

class Canvas(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.create_widget()

    def create_widget(self):
        pass
    
    # def move(self, x, y):
