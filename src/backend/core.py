import json
from .gameClass import Board, Vehicle

def map_loader(path, level):
    with open(path, 'r') as file:
        data = json.load(file)
        
    vehicles_level_data = data[level]
    
    vehicles = []
    for v in vehicles_level_data:
        vehicle = Vehicle(
            id=v['id'],
            pos=(v['row'], v['col']),
            rotation=v['rotation'],
            length=v['length']
        )
        vehicles.append(vehicle)
        
    board = Board(vehicles)
    return board 
        