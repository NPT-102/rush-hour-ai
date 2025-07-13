import json
import random
import multiprocessing

from logic.gameClass import Map, Vehicle

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
    attempts = 0
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

        if not any(
            take[row + (i if orientation == "V" else 0)][col + (i if orientation == "H" else 0)]
            for i in range(length)
        ):
            vehicles.append(new_vehicle)
            mark_vehicle([new_vehicle])
            candidate_ids.remove(temp_id)
            count_installed += 1

    return vehicles


def rate_level_map(maps: list[list[dict]]):
    map_scores = []

    for idx, vehicles_raw in enumerate(maps):
        state = tuple(tuple(v["pos"]) for v in vehicles_raw)
        vehicles = tuple(Vehicle(v["id"], v["length"], v["orientation"]) for v in vehicles_raw)
        m = Map(state, vehicles)

        score = len(vehicles)

        bfs_result = m.bfs()
        if bfs_result:
            bfs_path, _ = bfs_result
            score += (len(bfs_path) - 1) * 10

        ucs_result = run_with_timeout(m.ucs, timeout=30)
        if ucs_result:
            ucs_path, ucs_cost, _ = ucs_result
            if ucs_cost:
                score += ucs_cost[-1] * pow(10, len(str(score)))
        else:
            print(f"[TIMEOUT] UCS took too long at map {idx}")

        print(f"Map {idx + 1}: Score = {score}, Vehicles = {len(vehicles_raw)} cars")
        map_scores.append((score, vehicles_raw))

    map_scores.sort(key=lambda x: x[0])
    return map_scores


def generate_level_map(num_map):
    maps = []
    while len(maps) < num_map:
        num_v = random.randint(6, 9)
        print(f"Generating map with {num_v} vehicles...")
        vehicles = generate_challenging_map(num_v)
        print(f"Generated map with {len(vehicles)} vehicles.")
        score, vehicles_data = rate_level_map([vehicles])[0]
        maps.append((score, vehicles_data))

    maps.sort(key=lambda x: x[0])
    return maps


def generate_map_json(num_map):
    vehicles = generate_level_map(num_map)

    print("Scoring levels:")
    for i, (_, vlist) in enumerate(vehicles):
        print(f"Level {i + 1}: Vehicles = {len(vlist)} cars")

    with open('map.json', 'w') as f:
        json.dump(
            [{"level": i + 1, "vehicles": v} for i, (_, v) in enumerate(vehicles)],
            f, indent=4
        )
    print(f" Done generating map.json with {num_map} levels.")


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

    MAX_RETRY = 20
    for _ in range(MAX_RETRY):
        template = random.choice(TEMPLATES)
        valid = True
        for v in template:
            if not is_valid(v):
                valid = False
                break

        if valid:
            for v in template:
                vehicles.append(v)
                mark(v)
            break
    else:
        raise ValueError("Too many invalid template retries.")

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

def run_with_timeout(func, args=(), timeout=30):
    def wrapper(q, *args):
        try:
            result = func(*args)
            q.put(result)
        except Exception as e:
            q.put(None)

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=wrapper, args=(q, *args))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return None
    return q.get() if not q.empty() else None

if __name__ == "__main__":
    num_levels = 5
    generate_map_json(num_levels)
