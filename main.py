from Gui.app import RushHourApp
from Logic import core

map = "Map/map.json"

gui = RushHourApp(
    map_loader=core.map_loader,
    map=map,
    number_of_maps=10
)
gui.run()