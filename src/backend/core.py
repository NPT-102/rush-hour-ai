import json
from .gameClass import Map, Vehicle

def map_loader(path, level):
    if level is None:
        return None, None
    
    with open(path, 'r') as file:
        data = json.load(file)
        
    vehicles_level_data = data[level]['vehicles']
    
    vehicles = ()
    state = ()
    for v in vehicles_level_data:
        vehicle = Vehicle(
            v['id'],
            v['length'],
            v['orientation']
        )
        vehicles += (vehicle,)

        pos = tuple(v['pos'])
        state += (pos,)
        
    return state, vehicles
        