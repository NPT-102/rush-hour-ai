from gui.app import gui
from backend import core

map = "map.json"

gui(map_loader=core.map_loader, map=map)