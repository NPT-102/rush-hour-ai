import tkinter as tk
from .selector import Selector   
from .controls import ControlButtons
from .grid import Grid
from .stats import Stats
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
    step = -1
    cost = 0    

    # Callback functions
    def on_change(search_algo=None, costList=None):
        nonlocal step, cost
        step += 1
        if search_algo == "UCS":
            cost = costList[step]
        else:
            cost = step
            
    def on_map_select(map_id):
        nonlocal init_state, vehicles, m, step, cost
        init_state, vehicles = map_loader(map, int(map_id) - 1)
        m = Map(init_state, vehicles)
        grid.update(vehicles=vehicles, state=init_state)
        step = -1
        cost = 0
        stats.update_stats(step, cost)

    def on_search_select(search_algo):
        nonlocal states, cost
        if search_algo == "BFS":
            states = m.bfs()
        elif search_algo == "DFS":
            states = m.dfs()
        elif search_algo == "UCS":
            states, costList = m.ucs()
            
        for i, state in enumerate(states):
            on_change(search_algo=search_algo, costList=costList if search_algo == "UCS" else None)
            grid.clear_state()
            grid.update_state(state)
            stats.update_stats(step, cost)
            window.update()
            if i < len(states) - 1:
                window.after(1000)
            
        # Display the car get out the map
        origin_map = states[-1]
        out_map = []
        for i in range (0, 3):
            l = []
            for j in range(len(vehicles)):
                if j == 0:
                    l.append((origin_map[j][0], origin_map[j][1] + i))
                else:
                    l.append((origin_map[j][0], origin_map[j][1]))
            out_map.append(l)
            
        for i, state in enumerate(out_map):
            grid.clear_state()
            grid.update_state(state)
            window.update()
            if i < len(out_map) - 1:
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
    
    # Step and cost
    stats = Stats(parent=window, step=step, cost=cost)
    stats.pack(pady=10)

    # Create an instance of the Grid (empty at first)
    grid = Grid(parent=window, vehicles=vehicles, state=init_state)

    # Create an instance of ControlButtons
    controls = ControlButtons()
    controls.pack(pady=10)

    window.mainloop()
