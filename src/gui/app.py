import tkinter as tk
from tkinter import messagebox
import time

from gui.selector import Selector   
from gui.controls import ControlButtons
from gui.stats import Stats
from gui.gameDisplay import GameDisplay
from backend.gameClass import Map


class RushHourApp:
    def __init__(self, map_loader, map, number_of_maps=10):
        self.map_loader = map_loader
        self.map_file = map
        self.window = tk.Tk()
        self.window.title("Rush Hour")
        self.window.geometry("800x700")
        
        # Initial state
        self.init_state = None
        self.vehicles = None
        self.map_object = None
        self.states = None
        self.step = -1
        self.cost = 0
        self.search_time = 0
        self.is_running = False
        

        map_options = list(range(1, number_of_maps + 1))
        search_options = ["BFS", "DFS", "UCS", "A*"]
        self.selectors = Selector(
            parent=self.window,
            map_options=map_options,
            search_options=search_options,
            on_map_select=self.on_map_select,
            on_search_select=self.on_search_select
        )
        self.selectors.pack(pady=10)
        
        self.gameDisplay = GameDisplay(parent=self.window, vehicles=self.vehicles, state=self.init_state)
        self.gameDisplay.pack(pady=10)
        
        self.stats = Stats(parent=self.window, step=self.step, cost=self.cost)
        self.stats.pack(pady=10)

        self.controls = ControlButtons(
            parent=self.window,
            play_pause=self.play_pause,
            on_reset=self.reset
        )
        self.controls.pack(pady=10)

    
    def on_change(self):
        self.step += 1
        if self.search_algo == "UCS" or self.search_algo == "A*":
            self.cost = self.costList[self.step]
        else:
            self.cost = self.step
        self.stats.update_stats(self.step, self.cost)
            

    def on_map_select(self, map_id):
        self.map_id = map_id
        self.init_state, self.vehicles = self.map_loader(self.map_file, int(map_id) - 1)
        self.map_object = Map(self.init_state, self.vehicles)
        self.gameDisplay.update(vehicles=self.vehicles, state=self.init_state)
        self.step = -1
        self.cost = 0
        search_time = 0
        self.stats.update_time(search_time)
        self.stats.update_stats(self.step, self.cost)


    def on_search_select(self, search_algo):
        if self.map_object is None:
            messagebox.showwarning("Warning", "Please select a map first.")
            return

        self.reset()
        self.costList = []
        start_time = time.time()
        if search_algo == "BFS":
            self.states = self.map_object.bfs()
        elif search_algo == "DFS":
            self.states = self.map_object.dfs()
        elif search_algo == "UCS":
            self.states, self.costList = self.map_object.ucs()
        elif search_algo == "A*":
            self.states, self.costList = self.map_object.a_star()
        
        self.search_time = round(time.time() - start_time, 2)
        self.stats.update_time(self.search_time)
        self.search_algo = search_algo
        
        if self.states is None:
            messagebox.showinfo("Solution Not Found",
                                "No solution found for the selected map with the search algorithm. Please try a different map or algorithm.")
        
        self.is_running = True
        self.controls.toggled_play_pause(self.is_running)
        self.show_path()

    

    def show_path(self):
        if not self.is_running:
            return
        
        if self.step + 1 >= len(self.states):
            self.exit()
            return

        self.show_step()

        self.window.after(1000, lambda: self.show_path())
    

    def show_step(self):
            state = self.states[self.step + 1]
            self.on_change()
            self.gameDisplay.clear_state()
            self.gameDisplay.update_state(state)
            self.window.update()
        
    
    def exit(self, i=0):
        if i >= 3:
            return

        origin_map = self.states[-1]
        out_path = []
        for j in range(len(self.vehicles)):
            if j == 0:
                out_path.append((origin_map[j][0], origin_map[j][1] + i))
            else:
                out_path.append((origin_map[j][0], origin_map[j][1]))

        self.gameDisplay.clear_state()
        self.gameDisplay.update_state(out_path)
        self.window.after(1000, lambda: self.exit(i + 1))
    
    
    def play_pause(self):
        self.is_running = not self.is_running
        self.controls.toggled_play_pause(self.is_running)
        if self.is_running:
            self.show_path()
            
    
    def reset(self):
        self.is_running = False
        self.controls.toggled_play_pause(self.is_running)
        self.step = -1
        self.cost = 0
        self.stats.update_stats(self.step, self.cost)
        self.search_time = 0
        self.stats.update_time(self.search_time)
        self.gameDisplay.clear_state()
        self.gameDisplay.update(self.vehicles, self.init_state)


    def run(self):
        self.window.mainloop()