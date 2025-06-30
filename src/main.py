from backend import core
from backend.gameClass import Board
from backend.search import dfs

v = core.map_loader('map.json', 0)
b = Board(v)
for row in b.board:
    print(row)
print('\n')
 
a = []
c = set()
r = dfs(b, a, c)
if r:
    for board in r:
        for row in board.board:
            print(row)
        print('\n')
        print(a, '\n')
        print(c, '\n')
        