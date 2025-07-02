import tkinter as tk
from selector import Selector   
from controls import ControlButtons
from canvas import Canvas

window = tk.Tk()
window.title("Rush Hour")
window.geometry("800x500")

# Create an instance of Selector with example options
map_options = ["Map 1", "Map 2", "Map 3"]
search_options = ["Search 1", "Search 2", "Search 3"]
selectors = Selector(parent=window, map_options=map_options, search_options=search_options)
selectors.pack(pady=10)

# Create an instance of the Canvas
board = Canvas(parent=window)
board.pack(pady=10)

# Create an instance of ControlButton
controls = ControlButtons()
controls.pack(pady=10)

window.mainloop()