import tkinter as tk

class Stats(tk.Frame):
    def __init__(self, parent=None, step=0, cost=0, time=0, expanded_nodes=0, memory_usage=0):
        super().__init__(parent)
        self.parent = parent
        if step < 0:
            self.step = 0
        else:
            self.step = step
        self.cost = cost
        self.time = time
        self.expanded_nodes = expanded_nodes
        self.memory = memory_usage
        self.create_widget()

    def create_widget(self):
        tk.Label(self, text="Steps:").pack(side="left")
        self.step_label = tk.Label(self, text=str(self.step))
        self.step_label.pack(side="left")
        
        tk.Label(self, text="Cost:").pack(side="left", padx=(20, 0))
        self.cost_label = tk.Label(self, text=str(self.cost)) 
        self.cost_label.pack(side="left")
        
        tk.Label(self, text="Search Time:").pack(side="left", padx=(20, 0))
        self.time_label = tk.Label(self, text=str(self.time) + "s")
        self.time_label.pack(side="left")
        
        tk.Label(self, text="Memory Usage:").pack(side="left", padx=(20, 0))
        self.memory_label = tk.Label(self, text="0 KB")
        self.memory_label.pack(side="left")
        
        tk.Label(self, text="Expanded Nodes:").pack(side="left", padx=(20, 0))
        self.expanded_nodes_label = tk.Label(self, text=str(self.expanded_nodes))
        self.expanded_nodes_label.pack(side="left")
       
    def update_stats(self, step, cost):
        if step < 0:
            self.step = 0
        else:
            self.step = step
        self.cost = cost
        self.step_label.config(text=str(self.step))
        self.cost_label.config(text=str(self.cost))
        
    def update_time(self, time):
        self.time = time
        self.time_label.config(text=str(self.time) + "s")
        
    def update_expanded_nodes(self, expanded_nodes):
        self.expanded_nodes = expanded_nodes
        self.expanded_nodes_label.config(text=str(self.expanded_nodes))
        
    def update_memory(self, memory_usage):
        self.memory = memory_usage
        self.memory_label.config(text=f"{memory_usage / 1024 / 1024:.2f} MB")