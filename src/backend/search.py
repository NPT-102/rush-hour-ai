from .gameClass import Board

def dfs(board: Board, path: list, node: set):
    if board.is_finished():
        return path

    for vehicle in board.vehicles:
        if vehicle.id in node:
            continue
        node.add(vehicle.id)
        for step in [-1, 1]:
            for _ in range(1, 6):
                new_board = board.copyBoard().move(vehicle.id, step)
                if new_board:
                    result = dfs(new_board, path + [new_board], set(node))
                    if result:
                        return result
        node.remove(vehicle.id)

    return None
