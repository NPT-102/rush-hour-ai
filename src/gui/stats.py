import tkinter as tk

class Stats(tk.Frame):
    def __init__(self, parent=None, step=0, cost=0, time = 0):
        super().__init__(parent)
        self.parent = parent
        if step < 0:
            self.step = 0
        else:
            self.step = step
        self.cost = cost
        self.time = time;
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
        