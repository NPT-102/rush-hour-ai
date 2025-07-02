import tkinter as tk

class Car():
    colors = {
        0: "#e6194b",   # red
        1: "#3cb44b",   # green
        2: "#ffe119",   # yellow
        3: "#0082c8",   # blue
        4: "#f58231",   # orange
        5: "#911eb4",   # purple
        6: "#46f0f0",   # cyan
        7: "#f032e6",   # magenta
        8: "#d2f53c",   # lime
        9: "#fabebe",   # pink
        10: "#008080",  # teal
        11: "#e6beff",  # lavender
        12: "#aa6e28",  # brown
        13: "#fffac8",  # beige
        14: "#800000",  # maroon
        15: "#aaffc3"   # mint
    }

    # id would decide the color of the car
    # may change arguments later based on logic
    def __init__(self, canvas, id, x, y, length, orientation):
        self.canvas = canvas
        self.id = id
        self.x = x
        self.y = y
        self.length = length
        if (orientation == "horizontal"):
            self.image = self.draw_horizontal(x, y, length)
        elif (orientation == "vertical"):
            self.image = self.draw_vertical(x, y, length)
            

    def draw_horizontal(self, x, y, length):
        return self.canvas.create_rectangle(
            x * 60, y * 60, (x + length) * 60, (y + 1) * 60,
            fill=self.colors[self.id]
        )

    def draw_vertical(self, x, y, length):
        return self.canvas.create_rectangle(
            x * 60, y * 60, (x + 1) * 60, (y + length) * 60,
            fill=self.colors[self.id]
        )
        
    # Implement based on game logic
    def move(self):
        pass