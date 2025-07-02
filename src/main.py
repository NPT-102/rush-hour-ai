from backend import core
from backend.gameClass import Map

state, vehicles = core.map_loader('map.json', 0)
m = Map(state, vehicles)

#path = m.bfs()
#path = m.dfs()
path, cost = m.ucs()

for p, c in zip(path, cost):
	print(f"{p} - {c}")