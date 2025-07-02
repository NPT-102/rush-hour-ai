import tkinter as tk
from .selector import Selector   
from .controls import ControlButtons
# from .canvas import Canvas
from .grid import Grid

def gui(vehicles, state, map):
    window = tk.Tk()
    window.title("Rush Hour")
    window.geometry("800x700")

    # Create an instance of Selector with example options
    map_options = ["Map 1", "Map 2", "Map 3"]
    search_options = ["BFS", "DFS", "UCS"]
    selectors = Selector(parent=window, map_options=map_options, search_options=search_options)
    selectors.pack(pady=10)

    # Create an instance of the Canvas
    board = Grid(parent=window, vehicles=vehicles, state=state)
    # board.pack(pady=5)

    # Create an instance of ControlButton
    controls = ControlButtons()
    controls.pack(pady=10)

    window.mainloop()
    