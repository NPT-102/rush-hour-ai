import json
import random
from gameClass import Map, Vehicle

def generate_random_map(num_v):
    grid_size = 6
    row_goal = 2
    take = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    vehicles = []

    def mark_vehicle(vehicles):
        for v in vehicles:
            if v["orientation"] == "H":
                for i in range(v["length"]):
                    take[v["pos"][0]][v["pos"][1] + i] = 1
            else:
                for i in range(v["length"]):
                    take[v["pos"][0] + i][v["pos"][1]] = 1

    s_col = random.randint(0, grid_size - 2)
    car_S = {
        "id": "S",
        "length": 2,
        "pos": [row_goal, s_col],
        "orientation": "H"
    }
    vehicles.append(car_S)
    mark_vehicle([car_S])

    candidate_ids = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'S']
    count_installed = 1
    while count_installed < num_v:
        id = random.choice(candidate_ids)
        candidate_ids.remove(id)

        length = random.choice([2, 3])
        orientation = random.choice(["H", "V"])

        if orientation == "H":
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - length)
        else:
            row = random.randint(0, grid_size - length)
            col = random.randint(0, grid_size - 1)

        new_vehicle = {
            "id": id,
            "length": length,
            "pos": [row, col],
            "orientation": orientation
        }

        if not any(
            take[new_vehicle["pos"][0] + (i if orientation == "V" else 0)]
                [new_vehicle["pos"][1] + (i if orientation == "H" else 0)] 
            for i in range(length)
        ):
            vehicles.append(new_vehicle)
            mark_vehicle([new_vehicle])
            count_installed += 1
    return vehicles

def rate_level_map(maps: list[list[dict]]):
    map_scores = []

    for idx, vehicles_raw in enumerate(maps):
        # Load state & vehicles
        state = tuple(tuple(v["pos"]) for v in vehicles_raw)
        vehicles = tuple(Vehicle(v["id"], v["length"], v["orientation"]) for v in vehicles_raw)
        m = Map(state, vehicles)

        score = 0
        # 1. number of vehicles
        score += len(vehicles)

        # 2. BFS steps
        bfs_path = m.bfs()
        if bfs_path:
            score += (len(bfs_path) - 1) * 10
        # 3. UCS cost
        ucs_result = m.ucs()
        if ucs_result:
            _, ucs_cost = ucs_result
            score += ucs_cost[-1] * pow(10, len(bfs_path))

        map_scores.append((score, vehicles_raw))
    map_scores.sort(key=lambda x: x[0])

    return map_scores


def generate_level_map(num_map):
    map = []
    for _ in range(num_map):
        num_v = random.randint(2, 6)
        vehicles = generate_random_map(num_v)
        map.append(vehicles)
    map_sorted = rate_level_map(map)
    return map_sorted

def generate_map_json(num_map):
    vehicles = generate_level_map(num_map)
    with open('map.json', 'w') as f:
        json.dump(
            [{"level": i + 1, "vehicles": v} for i, (_, v) in enumerate(vehicles)],
            f, indent=4
        )

if __name__ == "__main__":
    generate_map_json(10) 
    print("Done generating map.json with 10 levels.")