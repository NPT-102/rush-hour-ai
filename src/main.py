from backend import core
from backend.gameClass import Map
from gui.app import gui

init_state, vehicles = core.map_loader('map.json', 0)
map = Map(init_state, vehicles)

# path = m.bfs()
# path = m.dfs()

# path, cost = m.ucs()

# for p, c in zip(path, cost):
# 	print(f"{p} - {c}")

gui(vehicles=vehicles, state=init_state, map=map)