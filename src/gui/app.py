import tkinter as tk
from .selector import Selector   
from .controls import ControlButtons
from .grid import Grid
from backend.gameClass import Map

def gui(map_loader, map):
    window = tk.Tk()
    window.title("Rush Hour")
    window.geometry("800x700")

    # Initial state
    init_state = None
    vehicles = None
    m = None
    states = None
    cost = None

    # Callback functions
    def on_map_select(map_id):
        nonlocal init_state, vehicles, m
        init_state, vehicles = map_loader(map, int(map_id) - 1)
        m = Map(init_state, vehicles)
        grid.update(vehicles=vehicles, state=init_state)

    def on_search_select(search_algo):
        nonlocal states, cost
        if search_algo == "BFS":
            states = m.bfs()
        elif search_algo == "DFS":
            states = m.dfs()
        elif search_algo == "UCS":
            states, cost = m.ucs()
            
        
        for i, state in enumerate(states):
            grid.clear_state()
            grid.update_state(state)
            window.update()
            if i < len(states) - 1:
                window.after(1000)

    map_options = list(range(1, 11))
    search_options = ["BFS", "DFS", "UCS"]
    selectors = Selector(
        parent=window,
        map_options=map_options,
        search_options=search_options,
        on_map_select=on_map_select,
        on_search_select=on_search_select
    )
    selectors.pack(pady=10)

    # Create an instance of the Grid (empty at first)
    grid = Grid(parent=window, vehicles=vehicles, state=init_state)

    # Create an instance of ControlButtons
    controls = ControlButtons()
    controls.pack(pady=10)

    window.mainloop()
