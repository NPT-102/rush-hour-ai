import tkinter as tk


class Selector(tk.Frame):
    def __init__(self, parent=None, map_options=None, search_options=None, on_map_select=None, on_search_select=None):
        super().__init__(parent)
        self.parent = parent
        self.on_map_select = on_map_select
        self.on_search_select = on_search_select
        self.create_widget(map_options, search_options)

    def create_widget(self, map_options, search_options):
        map_label = tk.Label(self, text="Map:")
        map_label.pack(side="left", padx=(10, 0))
        map_chosen = tk.StringVar()
        map_chosen.set(map_options[0])
        map_drop = tk.OptionMenu(self, map_chosen, *map_options)
        map_drop.pack(side="left", padx=(5, 0))
        mapBtn = tk.Button(self, text="Select", command=lambda: self.on_map_select(map_chosen.get()))
        mapBtn.pack(side="left", padx=(5, 0))

        search_label = tk.Label(self, text="Search:")
        search_label.pack(side="left", padx=(30, 0))
        search_chosen = tk.StringVar()
        search_chosen.set(search_options[0])
        search_drop = tk.OptionMenu(self, search_chosen, *search_options)
        search_drop.pack(side="left", padx=(5, 0))
        searchBtn = tk.Button(self, text="Search", command=lambda: self.on_search_select(search_chosen.get()))
        searchBtn.pack(side="left", padx=(5, 0))