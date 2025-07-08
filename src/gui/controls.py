import tkinter as tk

class ControlButtons(tk.Frame):
    def __init__(self, parent=None, on_previous=None, play_pause=None, on_next=None, on_reset=None):
        super().__init__(parent)
        self.parent = parent
        self.on_previous = on_previous
        self.play_pause = play_pause
        self.on_next = on_next
        self.on_reset = on_reset
        self.create_widget()


    def create_widget(self):
        self.play_pause = tk.Button(self, text="▶", command=self.play_pause)
        self.play_pause.pack(side="left")
        tk.Button(self, text="Reset", command=self.on_reset).pack(side="right", padx=(20, 0))


    def toggled_play_pause(self, is_play):
        new_text = "⏸" if is_play else "▶"
        self.play_pause.config(text=new_text)
        