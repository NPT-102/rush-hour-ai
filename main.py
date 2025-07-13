from gui.app import RushHourApp
from logic import core

map = "map/map.json"

gui = RushHourApp(
    map_loader=core.map_loader,
    map=map,
    number_of_maps=10
)
gui.run()