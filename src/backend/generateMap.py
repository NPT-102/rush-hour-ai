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

    # Add red car
    s_col = random.randint(0, grid_size - 4)
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
    attempts = 0  # avoid infinite loop
    max_attempts = 1000

    while count_installed < num_v and attempts < max_attempts and candidate_ids:
        attempts += 1
        temp_id = random.choice(candidate_ids)
        length = random.choice([2, 3])
        orientation = random.choice(["H", "V"])

        if orientation == "H":
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - length)
        else:
            row = random.randint(0, grid_size - length)
            col = random.randint(0, grid_size - 1)

        if orientation == "H" and row == row_goal:
            continue

        new_vehicle = {
            "id": temp_id,
            "length": length,
            "pos": [row, col],
            "orientation": orientation
        }

        # Check no overlap
        if not any(
            take[row + (i if orientation == "V" else 0)][col + (i if orientation == "H" else 0)]
            for i in range(length)
        ):
            vehicles.append(new_vehicle)
            mark_vehicle([new_vehicle])
            candidate_ids.remove(temp_id)  # only remove when placed successfully
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
        # # 1. number of vehicles
        score += len(vehicles)

        # # 2. BFS steps
        bfs_path = m.bfs()
        if bfs_path:
            score += (len(bfs_path) - 1) * 10
        # # 3. UCS cost
        ucs_result = m.ucs()
        if ucs_result:
            _, ucs_cost = ucs_result
            score += ucs_cost[-1] * pow(10, len(str(score)))

        

        map_scores.append((score, vehicles_raw))
    map_scores.sort(key=lambda x: x[0])

    return map_scores


def generate_level_map(num_map):
    map = []
    while len(map) < num_map:
        num_v = random.randint(4, 9)
        vehicles = generate_random_map(num_v)

        map_with_score = rate_level_map([vehicles])[0]
        score, vehicles_data = map_with_score

        
        map.append((score, vehicles_data))

    map.sort(key=lambda x: x[0])  # Keep the map sorted by score
    return map

def generate_map_json(num_map):
    vehicles = generate_map_with_exact_steps(15, algo='bfs', max_attempts=10000)
    
    print("Scoring levels:")
    for i, v in enumerate(vehicles):
        print(f"Level {i + 1}: Vehicles = {len(v)} cars")
    
    with open('map.json', 'w') as f:
        json.dump(
            [{"level": i + 1, "vehicles": v} for i, (_, v) in enumerate(vehicles)],
            f, indent=4
        )





with open("templates.json") as f:
    TEMPLATES = json.load(f)

def generate_challenging_map(num_v=6):
    grid_size = 6
    row_goal = 2
    take = [[0] * grid_size for _ in range(grid_size)]
    vehicles = []

    def mark(vehicle):
        i, j = vehicle["pos"]
        for k in range(vehicle["length"]):
            r = i + (k if vehicle["orientation"] == "V" else 0)
            c = j + (k if vehicle["orientation"] == "H" else 0)
            take[r][c] = 1

    def is_valid(vehicle):
        i, j = vehicle["pos"]
        for k in range(vehicle["length"]):
            r = i + (k if vehicle["orientation"] == "V" else 0)
            c = j + (k if vehicle["orientation"] == "H" else 0)
            if r >= grid_size or c >= grid_size or take[r][c] != 0:
                return False
        return True
    
    # Chọn ngẫu nhiên một template
    template = random.choice(TEMPLATES)
    

    for v in template:
        if not is_valid(v):
            print(f"[SKIP] Invalid template: vehicle {v['id']} at {v['pos']}")
            return generate_challenging_map()

        vehicles.append(v)
        mark(v)

    # Fillers (ngẫu nhiên) để tăng độ nhiễu
    candidate_ids = [chr(i) for i in range(ord('D'), ord('Z') + 1) if chr(i) not in ['S', 'A', 'B', 'C']]
    random.shuffle(candidate_ids)

    attempts = 0
    while len(vehicles) < num_v and attempts < 100 and candidate_ids:
        vid = candidate_ids.pop()
        length = random.choice([2, 3])
        orientation = random.choice(["H", "V"])

        if orientation == "H":
            i = random.randint(0, grid_size - 1)
            j = random.randint(0, grid_size - length)
        else:
            i = random.randint(0, grid_size - length)
            j = random.randint(0, grid_size - 1)

        new_vehicle = {
            "id": vid,
            "length": length,
            "pos": [i, j],
            "orientation": orientation
        }

        if is_valid(new_vehicle):
            vehicles.append(new_vehicle)
            mark(new_vehicle)

        attempts += 1

    return vehicles


def generate_map_with_exact_steps(k: int, algo: str = 'bfs', max_attempts=100000):
    while True:
        num_v= random.randint(7, 9)
        vehicles = generate_random_map(num_v)  # dùng hàm bạn đã có
        state = tuple(tuple(v["pos"]) for v in vehicles)
        vehicle_objs = tuple(Vehicle(v["id"], v["length"], v["orientation"]) for v in vehicles)
        m = Map(state, vehicle_objs)

        # chọn thuật toán
        if algo == 'bfs':
            result = m.bfs()
        elif algo == 'dfs':
            result = m.dfs()
        elif algo == 'ucs':
            result = m.ucs()
            result = result[0] if result else None
        elif algo == 'a_star':
            result = m.a_star()
            result = result[0] if result else None
        else:
            raise ValueError("Invalid algorithm")

        if result and len(result) - 1 >= k:
            print(f"✔ Found map with exactly {k} steps using {algo} ")
            return vehicles

    raise ValueError(f"❌ Cannot generate map with {k} steps using {algo} after {max_attempts} attempts.")



if __name__ == "__main__":
    generate_map_json(10) 
    print("Done generating map.json with 10 levels.")