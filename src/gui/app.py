import tkinter as tk

window = tk.Tk()
window.title("Rush Hour")


# Import the Selector class from selector.py
from selector import Selector   
# Create an instance of Selector with example options
map_options = ["Map 1", "Map 2", "Map 3"]
search_options = ["Search 1", "Search 2", "Search 3"]
selector = Selector(parent=window, map_options=map_options, search_options=search_options)
selector.pack(pady=10)


# Import the ControlButton class from controls.py
from controls import ControlButtons
# Create an instance of ControlButton
reset_button = ControlButtons()
reset_button.pack(pady=10)

window.mainloop()