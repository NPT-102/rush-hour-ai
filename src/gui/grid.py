from PIL import Image, ImageTk
import tkinter as tk

class Grid:
    def __init__(self, parent):
        self.parent = parent
        self.rows = 6
        self.cols = 6
        self.cell_size = 60
        self.canvas = tk.Canvas(parent, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg="lightgray")
        self.canvas.pack()
        
        self.cell_squares = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_grid()
        
    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                square = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline="black")
                self.cell_squares[r][c] = square
            