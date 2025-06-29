class Vehicle:
    def __init__(self, id: str, pos: tuple[int, int], rotation: str, length: int):
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
        
        if rotation not in ("horizontal", "vertical"):
            raise ValueError("Rotation must be 'horizontal' or 'vertical'")
        else:
            self.rotation = rotation
        
    
class Board:
    def __init__(self, vehicles: list[Vehicle], rows=6, cols=6):
        self.rows = rows
        self.cols = cols
        self.vehicles = vehicles
        self.init_board()

    def init_board(self):
        self.board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        for vehicle in self.vehicles:
            if vehicle.rotation == "horizontal":
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
                if vehicle.rotation == "horizontal":
                    if vehicle.pos[0] == 2 and vehicle.pos[1] + vehicle.length - 1 == 5:
                        return True
        return False
    
    def copyBoard(self):
        v = []
        for vehicle in self.vehicles:
            v.append(Vehicle(vehicle.id, vehicle.pos, vehicle.rotation, vehicle.length))
        return Board(v)
    
    def move(self, id: str, steps=1):
        for v in self.vehicles:
            if v.id == id:
                vehicle = v
                break
        if not vehicle:
            raise ValueError(f"Vehicle with ID {id} not found")
        
        if vehicle.rotation == "horizontal":
            new_col = vehicle.pos[1] + steps
            vehicle.pos = (vehicle.pos[0], new_col)
        else:
            new_row = vehicle.pos[0] + steps
            vehicle.pos = (new_row, vehicle.pos[1])
            
            
        # check if the new position is out of bounds
        if vehicle.rotation == 'horizontal':
            if new_col < 0 or new_col + vehicle.length > self.cols:
                return None
        else:
            if new_row < 0 or new_row + vehicle.length > self.rows:
                return None
        # check if the new position is occupied
        if vehicle.rotation == "horizontal":
            for i in range(vehicle.length):
                s = self.board[vehicle.pos[0]][new_col + i]
                if s != vehicle.id and s != '.':
                    return None            
        else:
            for i in range(vehicle.length):
                s = self.board[new_row + i][vehicle.pos[1]]
                if s != vehicle.id and s != '.':
                    return None
            
        return Board(self.vehicles)
            