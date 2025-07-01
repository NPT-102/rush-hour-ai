import tkinter as tk
from tkinter import Button

class ControlButtons(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.create_widget()

    def create_widget(self):
        Button(self, text="Previous", command=lambda: print("Previous action")).pack(side="left")
        Button(self, text="Play/Pause", command=lambda: print("Play/Pause action")).pack(side="left")
        Button(self, text="Next", command=lambda: print("Next action")).pack(side="left")
        Button(self, text="Reset", command=self.reset_game).pack(side="right", padx=(20, 0))

    def previous_step(self):
        print("Previous step")

    def play_pause(self):
        print("Play/Pause")

    def next_step(self):
        print("Next step")

    def reset_game(self):
        print("Game reset")
