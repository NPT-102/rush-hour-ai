from copy import deepcopy

class Vehicle:
    def __init__(self, id: str, pos: tuple[int, int], orientation: str, length: int):
        if type(id) is not str:
            raise TypeError("Vehicle ID must be a string")
        else:
            self.id = id
        
        if length not in (2, 3):
            raise ValueError("Vehicle length must be 2 or 3")
        else: 
            self.length = length
        
        if (pos[0] < 0 or pos[0] >= 6) or (pos[1] < 0 or pos[1] >= 6):
            raise ValueError("Position must be within the grid (0-5, 0-5)")
        else:
            self.pos = pos
        
        if orientation not in ("horizontal", "vertical"):
            raise ValueError("orientation must be 'horizontal' or 'vertical'")
        else:
            self.orientation = orientation
        
    
class Board:
    def __init__(self, vehicles: list[Vehicle], rows=6, cols=6):
        self.rows = rows
        self.cols = cols
        self.vehicles = vehicles
        self.init_board()

    def init_board(self):
        self.board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        for vehicle in self.vehicles:
            if vehicle.orientation == "horizontal":
                for i in range(vehicle.length):
                    self.board[vehicle.pos[0]][vehicle.pos[1] + i] = vehicle.id
            else:
                for i in range(vehicle.length):
                    self.board[vehicle.pos[0] + i][vehicle.pos[1]] = vehicle.id
    
                    
    def clear_board(self):
        self.board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        
    def is_finished(self):
        for vehicle in self.vehicles:
            if vehicle.id == "X":
                if vehicle.orientation == "horizontal":
                    if vehicle.pos[0] == 2 and vehicle.pos[1] + vehicle.length - 1 == 5:
                        return True
        return False
    
    def copyBoard(self):
        v = deepcopy(self.vehicles)
        return Board(v)
    
    #def move(self, id: str, steps=1):
    #    for v in self.vehicles:
    #        if v.id == id:
    #            vehicle = v
    #            break
    #    if not vehicle:
    #        raise ValueError(f"Vehicle with ID {id} not found")
    #    
    #    if vehicle.orientation == "horizontal":
    #        new_col = vehicle.pos[1] + steps
    #        vehicle.pos = (vehicle.pos[0], new_col)
    #    else:
    #        new_row = vehicle.pos[0] + steps
    #        vehicle.pos = (new_row, vehicle.pos[1])
    #        
    #        
    #    # check if the new position is out of bounds
    #    if vehicle.orientation == 'horizontal':
    #        if new_col < 0 or new_col + vehicle.length > self.cols:
    #            return None
    #    else:
    #        if new_row < 0 or new_row + vehicle.length > self.rows:
    #            return None
    #    # check if the new position is occupied
    #    if vehicle.orientation == "horizontal":
    #        for i in range(vehicle.length):
    #            s = self.board[vehicle.pos[0]][new_col + i]
    #            if s != vehicle.id and s != '.':
    #                return None            
    #    else:
    #        for i in range(vehicle.length):
    #            s = self.board[new_row + i][vehicle.pos[1]]
    #            if s != vehicle.id and s != '.':
    #                return None
    #        
    #    return Board(self.vehicles)
            
    def move(self, id: str, step=1):
        if step not in [-1, 1]:
            raise ValueError("Must take only 1 step at a time")
        
        vehicles = deepcopy(self.vehicles)
        
        for v in vehicles:
            if v.id == id:
                vehicle = v
                break
        else:
            raise ValueError("ID not exist")
        
        i, j = vehicle.pos

        if vehicle.orientation == "horizontal":
            start, end = j, j + vehicle.length
            if (step == 1) and (end >= self.cols or self.board[i][end] != '.'):
                return None
            if (step != 1) and (start <= 0 or self.board[i][start - 1] != '.'):
                return None
            
            vehicle.pos = (i, j + step)
            
        else:
            start, end = i, i + vehicle.length
            if (step == 1) and (end >= self.rows or self.board[end][j] != '.'):
                return None
            if (step != 1) and (start <= 0 or self.board[start - 1][j] != '.'):
                return None
            
            vehicle.pos = (i + step, j)

        return Board(vehicles)
