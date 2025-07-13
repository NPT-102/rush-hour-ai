import tkinter as tk
from PIL import Image, ImageTk

PADDING = 70

class GameDisplay(tk.Frame):
    def __init__(self, parent, vehicles, state):
        super().__init__(parent)
        self.vehicles = vehicles
        self.state = state
        self.rows = 8
        self.cols = 9
        self.cell_size = 70
        self.canvas = tk.Canvas(parent, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()
        
        self.set_background()
        if state is not None:
            self.set_assets()
            self.set_vehicles()
        
    def set_background(self):
        board_img = Image.open("Assets/board.png")
        self.board_img = ImageTk.PhotoImage(board_img)
        
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.board_img)
        
    def set_vehicles(self):
        for i in range(len(self.vehicles)):
            x = PADDING + (self.state[i][1]) * self.cell_size
            y = PADDING + (self.state[i][0]) * self.cell_size

            self.canvas.create_image(x, y, anchor=tk.NW, image=self.imgs[i])
            
    def set_assets(self):
        self.imgs = []
        for i in range(len(self.vehicles)):
            dir = "Assets/"
            if self.vehicles[i].id == 'S':
                dir = dir + "S.png"
            else:
                if self.vehicles[i].len == 2:
                    dir = dir + "two-" + str(i % 3) + ".png"
                elif self.vehicles[i].len == 3:
                    dir = dir + "three-" + str(i % 3) + ".png"
                    
            img = Image.open(dir)
            if self.vehicles[i].ori == 'H':
                img = img.rotate(pow(-1, (i + 1) % 2) * 90, expand=True)
            elif self.vehicles[i].ori == 'V':
                img = img.rotate((i % 2) * 180, expand=True)
            img = ImageTk.PhotoImage(img)
            self.imgs.append(img)
    
    def update_state(self, new_state):
        self.state = new_state
        self.set_vehicles()
        
    def update(self, vehicles, state):
        self.vehicles = vehicles
        self.state = state
        self.set_assets()
        self.set_vehicles()
        
    def clear_state(self):
        self.canvas.delete("all")
        self.set_background()
        