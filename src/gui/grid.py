import tkinter as tk
from PIL import Image, ImageTk

class Grid:
    def __init__(self, parent):
        self.parent = parent
        self.rows = 8
        self.cols = 9
        self.cell_size = 70
        self.canvas = tk.Canvas(parent, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()
        
        self.cell_squares = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.set_bg()
        # self.create_grid()
        
    def set_bg(self):
        board_img = Image.open("assets/board.png")
        self.board_img = ImageTk.PhotoImage(board_img)
        
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.board_img)
        
    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c* self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                square = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline="black")
                self.cell_squares[r][c] = square
            