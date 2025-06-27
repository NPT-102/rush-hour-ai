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
        
        if (pos[0] < 0 and pos[0] >= 6) or (pos[1] < 0 and pos[1] >= 6):
            raise ValueError("Position must be within the grid (0-5, 0-5)")
        else:
            self.pos = pos
        
        if rotation not in ("horizontal", "vertical"):
            raise ValueError("Rotation must be 'horizontal' or 'vertical'")
        else:
            self.rotation = rotation
        
    
    def get_id(self) -> str:
        return self.id
    
    def get_position(self) -> tuple[int, int]:
        return self.pos
    
    def get_rotation(self) -> str:
        return self.rotation
    
    def get_length(self) -> int:
        return self.length
    
class Board:
    def __intit__(self, vehicles: list[Vehicle]):
        self.vehicles = vehicles
        
    def get_vehicles(self) -> list[Vehicle]:
        return self.vehicles