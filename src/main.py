from gui.app import RushHourApp
from backend import core

map = "map.json"

gui = RushHourApp(
    map_loader=core.map_loader,
    map=map,
    number_of_maps=10
)
gui.run()