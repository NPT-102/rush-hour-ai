import tkinter as tk
from tkinter import messagebox
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
    def found_no_solution():
        messagebox.showinfo("Solution Not Found", "No solution found for the selected map with the search algorithm. Please try a different map or algorithm.")
    
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
        if m is None:
            messagebox.showwarning("Warning", "Please select a map first.")
            return
        nonlocal states, cost
        if search_algo == "BFS":
            states = m.bfs()
        elif search_algo == "DFS":
            states = m.dfs()
        elif search_algo == "UCS":
            states, costList = m.ucs()
        elif search_algo == "A*":
            states, costList = m.a_star()
         
        if states is not None:
            
            def path(i=0):
                if i < len(states):
                    if controls.is_playing.get():
                        on_change(search_algo=search_algo, costList=costList if search_algo in ["UCS", "A*"] else None)
                        grid.clear_state()
                        grid.update_state(states[i])
                        stats.update_stats(step, cost)
                        window.update()
                        window.after(1000, lambda: path(i + 1))
                    else:
                        window.after(100, lambda: path(i))
                else:            
                    messagebox.showinfo("Search Complete", f"Search completed using {search_algo}. Total steps: {step}, Total cost: {cost}.")
                    exit()       
            
            # Display the car get out the map
            def exit(i=0):
                if i >= 3:
                    return

                origin_map = states[-1]
                out_path = []
                for j in range(len(vehicles)):
                    if j == 0:
                        out_path.append((origin_map[j][0], origin_map[j][1] + i))
                    else:
                        out_path.append((origin_map[j][0], origin_map[j][1]))

                grid.clear_state()
                grid.update_state(out_path)
                window.after(1000, lambda: exit(i + 1))
        else:
            found_no_solution()
        path()        
            
    def reset_game():
        nonlocal init_state, vehicles, m, step, cost, states
        init_state = None
        vehicles = None
        m = None
        states = None
        step = -1
        cost = 0
        grid.clear_state()
        stats.update_stats(step, cost)
        messagebox.showinfo("Game Reset", "The game has been reset.")

    map_options = list(range(1, 11))
    search_options = ["BFS", "DFS", "UCS", "A*"]
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
    controls = ControlButtons(reset_game=reset_game)
    controls.pack(pady=10)

    window.mainloop()