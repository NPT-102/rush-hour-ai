from backend import core
from backend.gameClass import Board

v = core.map_loader('map.json', 0)
b = Board(v)
for row in b.board:
    print(row)
print('\n')
c = b.move('r', -1)
if c == None:
    print("Invalid move")
else:
    for row in c.board:
        print(row)