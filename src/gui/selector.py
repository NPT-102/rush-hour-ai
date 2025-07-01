import tkinter as tk


class Selector(tk.Frame):
    def __init__(self, parent=None, map_options=None, search_options=None):
        super().__init__(parent)
        self.parent = parent
        self.create_widget(map_options, search_options)

    def create_widget(self, map_options, search_options):
        map_chosen = tk.StringVar()
        map_chosen.set(map_options[0])

        map_drop = tk.OptionMenu(self, map_chosen, *map_options)
        map_drop.pack(side="left", padx=(20, 0))

        search_chosen = tk.StringVar()
        search_chosen.set(search_options[0])
        search_drop = tk.OptionMenu(self, search_chosen, *search_options)
        search_drop.pack(side="left", padx=(20, 0))

        mybutton = tk.Button(self, text="Select", command=lambda: self.selected(map_chosen.get(), search_chosen.get()))
        mybutton.pack(side="left", padx=(20, 0))

    def selected(self, map_value, search_value):
        print(f"Selected map: {map_value}, search: {search_value}")