import tkinter as tk
from tkinter import Canvas
import random
from PIL import Image, ImageTk

PADDING = 70

class Grid(Canvas):
    def __init__(self, parent, vehicles, state):
        super().__init__(parent)
        self.vehicles = vehicles
        self.state = state
        self.rows = 8
        self.cols = 9
        self.cell_size = 70
        self.canvas = tk.Canvas(parent, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()
        
        self.random_assets()
        self.set_bg()
        self.set_vehicles()
        
    def set_bg(self):
        board_img = Image.open("gui/assets/board.png")
        self.board_img = ImageTk.PhotoImage(board_img)
        
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.board_img)
        
    def set_vehicles(self):
        for i in range(len(self.vehicles)):
            vehicle = self.vehicles[i]
            img = Image.open(self.imgs[i])
            
            if vehicle.ori == 'H':
                img = img.rotate(-90, expand=True)
                
            tk_img = ImageTk.PhotoImage(img)
            self.imgs[i] = tk_img
            
            x = PADDING + (self.state[i][1]) * self.cell_size
            y = PADDING + (self.state[i][0]) * self.cell_size

            self.canvas.create_image(x, y, anchor=tk.NW, image=self.imgs[i])
            
    def random_assets(self):
        self.imgs = []
        dir = "gui/assets/"
        for i in range(len(self.vehicles)):
            if self.vehicles[i].id == 'S':
                self.imgs.append(dir + "S.png")
            else:
                if self.vehicles[i].len == 2:
                    ran = random.randint(0, 2)
                    self.imgs.append(dir + "two-" + str(ran) + ".png")
                elif self.vehicles[i].len == 3:
                    ran = random.randint(0, 2)
                    self.imgs.append(dir + "three-" + str(ran) + ".png")
                    
    def update_state(self, new_state):
        self.state = new_state
        self.set_vehicles()