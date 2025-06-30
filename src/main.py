from backend import core
from backend.gameClass import Map

state, vehicles = core.map_loader('map.json', 0)
m = Map(state, vehicles)

#path = m.bfs()
path = m.dfs()

for x in path:
	print(x)