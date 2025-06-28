from backend import core

b = core.map_loader('map.json', 0)

for row in b.board:
    print(row)