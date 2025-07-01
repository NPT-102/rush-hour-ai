import tkinter as tk
from selector import Selector   
from controls import ControlButtons
from grid import Grid

window = tk.Tk()
window.title("Rush Hour")
window.geometry("800x500")

# Create an instance of Selector with example options
map_options = ["Map 1", "Map 2", "Map 3"]
search_options = ["Search 1", "Search 2", "Search 3"]
selector = Selector(parent=window, map_options=map_options, search_options=search_options)
selector.pack(pady=10)

# Create an instance of Board with a specific size
board = Grid(window)

# Create an instance of ControlButton
reset_button = ControlButtons()
reset_button.pack(pady=10)

window.mainloop()