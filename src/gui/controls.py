import tkinter as tk

class ControlButtons(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.create_widget()

    def create_widget(self):
        tk.Button(self, text="Previous", command=self.previous_step).pack(side="left")
        tk.Button(self, text="Play/Pause", command=self.play_pause).pack(side="left")
        tk.Button(self, text="Next", command=self.next_step).pack(side="left")
        tk.Button(self, text="Reset", command=self.reset_game).pack(side="right", padx=(20, 0))

    def previous_step(self):
        print("Previous step")

    def play_pause(self):
        print("Play/Pause")

    def next_step(self):
        print("Next step")

    def reset_game(self):
        print("Game reset")
