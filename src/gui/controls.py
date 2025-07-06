import tkinter as tk

class ControlButtons(tk.Frame):
    def __init__(self, parent=None, reset_game=None):
        super().__init__(parent)
        self.parent = parent
        self.reset_game = reset_game
        self.is_playing = tk.BooleanVar(value=True)
        self.create_widget()

    def create_widget(self):
        self.play_pause = tk.Button(self, text="Play", command=self.toggle_play_pause)
        self.play_pause.pack(side="left")
        tk.Button(self, text="Reset", command=self.reset_game).pack(side="right", padx=(20, 0))

    def toggle_play_pause(self):
        self.is_playing.set(not self.is_playing.get())
        new_text = "Pause" if self.is_playing.get() else "Play"
        self.play_pause.config(text=new_text)