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
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for vehicle in self.vehicles:
            if vehicle.rotation == "horizontal":
                for i in range(vehicle.length):
                    self.board[vehicle.pos[0]][vehicle.pos[1] + i] = vehicle.id
            else:
                for i in range(vehicle.length):
                    self.board[vehicle.pos[0] + i][vehicle.pos[1]] = vehicle.id
        for i in range (self.rows):
            for j in range(self.cols):
                if self.board[i][j] is None:
                    self.board[i][j] = "."
    
                    
    def clear_board(self):
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]