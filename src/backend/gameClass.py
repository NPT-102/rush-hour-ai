from collections import deque
import heapq

class Vehicle:
	def __init__(self, id: str, len: int, orientation: str):
		self.id = id
		self.len = len
		self.ori = orientation

	def __str__(self):
		return f"[{self.len}, {self.ori}]"

class Map:
	def __init__(self, state: tuple[tuple[int, int]], vehicles: tuple[Vehicle]):
		# The targeted car must be at the index 0
		if vehicles[0].ori != "H":
			raise ValueError("The targeted car has to be horizontal")
 
		self.vehicles = vehicles
		if not self.validate(state):
			raise ValueError("The initial state is not valid")
		
		self.init_state = state
		self.target = self.vehicles[0]

	def validate(self, state:tuple[tuple[int, int]]):
		grid = [[0 for _ in range(6)] for _ in range(6)]
		
		for index in range(len(self.vehicles)):
			pos, vehicle = state[index], self.vehicles[index]

			i, j = pos
			if (i < 0 or i >= 6) or (j < 0 or j >= 6): return False

			if vehicle.ori == "H":
				if j + vehicle.len > 6: return False
				for jdx in range(j, j + vehicle.len):
					if grid[i][jdx] != 0: return False
					grid[i][jdx] = 1
			else:
				if i + vehicle.len > 6: return False
				for idx in range(i, i + vehicle.len):
					if grid[idx][j] != 0: return False
					grid[idx][j] = 1
					
		return True
	
	def generate_move(self, state: tuple[tuple[int, int]]) -> list[tuple[int, tuple[int, int]]]:
		generated_move = []

		for i in range(len(self.vehicles)):
			for step in [-1, 1]:
				mutable_state = list(state)

				if self.vehicles[i].ori == "H":
					mutable_state[i] = (state[i][0], state[i][1] + step)
				else:
					mutable_state[i] = (state[i][0] + step, state[i][1])

				new_state = tuple(mutable_state)
				if self.validate(new_state):
					generated_move.append((i, new_state))
		
		return generated_move

	def is_goal(self, state: tuple[int, int]) -> bool:
		return state[0][1] == 4
	
	def bfs(self, init_state = None) -> list[tuple[tuple[int, int]]]:
		if init_state is None:
			init_state = self.init_state
		expanded_nodes = 0
		visited = set()
		frontiers = deque([init_state])
		parents = {init_state: None}

		while frontiers:
			current = frontiers.popleft()
			visited.add(current)

			if self.is_goal(current):
				path = []
				while current is not None:
					path.append(current)
					current = parents[current]
				return path[::-1], expanded_nodes

			for i, state in self.generate_move(current):
				if state not in visited:
					expanded_nodes += 1
					parents[state] = current
					frontiers.append(state)

		return None, 0

	def dfs(self) -> list[tuple[tuple[int, int]]]:
		expanded_nodes = 0
		visited = set()
		frontiers = deque([self.init_state])
		parents = {self.init_state: None}

		while frontiers:
			current = frontiers.pop()
			visited.add(current)

			if self.is_goal(current):
				path = []
				while current is not None:
					path.append(current)
					current = parents[current]
				return path[::-1], expanded_nodes

			for i, state in self.generate_move(current):
				if state not in visited:
					expanded_nodes += 1
					parents[state] = current
					frontiers.append(state)

		return None, 0

	def ucs(self) -> list:
		expanded_nodes = 0
		frontiers = [(0, self.init_state)]
		parents = {self.init_state: None}
		true_cost = {self.init_state: 0}

		while frontiers:
			curr_cost, curr_state = heapq.heappop(frontiers)
			if curr_cost > true_cost[curr_state]:
				continue

			if self.is_goal(curr_state):
				path = []
				cost = []
				while curr_state is not None:
					path.append(curr_state)
					cost.append(true_cost[curr_state])
					curr_state = parents[curr_state]
				return path[::-1], cost[::-1], expanded_nodes

			for i, state in self.generate_move(curr_state):
				cost = curr_cost + self.vehicles[i].len
				if state not in true_cost or true_cost[state] > cost:
					expanded_nodes += 1
					true_cost[state] = cost
					heapq.heappush(frontiers, (cost, state))
					parents[state] = curr_state
		
		return None, None, 0
	
	def blocking_chain_depth(self, state, inx_blocker, visited=None, depth=1)->int:
		if visited is None:
			visited = set()

		if inx_blocker in visited:
			return float("inf")

		for move_state in self.bfs(state):
			if move_state[inx_blocker] != state[inx_blocker]:
				return depth
			
		visited.add(inx_blocker)
		blocker = self.vehicles[inx_blocker]
		i, j = state[inx_blocker]
		blocked_positions = []
		if blocker.ori == "H":
			for c in range(j, j + blocker.len):
				blocked_positions.append((i, c))
		else:
			for r in range(i, i + blocker.len):
				blocked_positions.append((r, j))
		
		for pos in blocked_positions:
			for idx in range(1, len(self.vehicles)):
				if idx == inx_blocker:
					continue
				Vi, Vj = state[idx]
				V = self.vehicles[idx]
				if V.ori == "H":
					for c in range(Vj, Vj + V.len):
						if (Vi, c) == pos:
							return self.blocking_chain_depth(state, idx, visited, depth + 1)
				else:
					for r in range(Vi, Vi + V.len):
						if (r, Vj) == pos:
							return self.blocking_chain_depth(state, idx, visited, depth + 1)
		return depth + 1

	def heuristic(self, state: tuple[tuple[int, int]]) -> int:
		target_i, target_j = state[0]
		s_len = self.vehicles[0].len
		score = 0

		for col in range(target_j + s_len, 6):
			pos = (target_i, col)
			blocker_idx = None
			for idx in range(1, len(self.vehicles)):
				
				Vi, Vj = state[idx]
				V = self.vehicles[idx]
				if V.ori == "H":
					for c in range(Vj, Vj + V.len):
						if (Vi, c) == pos:
							blocker_idx = idx
							break
				else:
					for r in range(Vi, Vi + V.len):
						if (r, Vj) == pos:
							blocker_idx = idx
							break
				if blocker_idx is not None:
					break
			if blocker_idx is not None:
				score += 1

				can_escape = False
				for move_state in self.bfs(state):
					if move_state[blocker_idx] != state[blocker_idx]:
						can_escape = True
						break
					if not can_escape:
						score += self.blocking_chain_depth(state, blocker_idx) * 10
		
		return score

	def a_star(self):
		expanded_nodes = 0
		frontiers = [(self.heuristic(self.init_state), self.init_state)]
		parents = {self.init_state: None}
		true_cost = {self.init_state: 0}

		while frontiers:
			curr_cost, curr_state = heapq.heappop(frontiers)
			if curr_cost > true_cost[curr_state]:
				continue

			if self.is_goal(curr_state):
				path = []
				cost = []
				while curr_state is not None:
					path.append(curr_state)
					cost.append(true_cost[curr_state])
					curr_state = parents[curr_state]
				return path[::-1], cost[::-1], expanded_nodes

			for i, state in self.generate_move(curr_state):
				cost = true_cost[curr_state] + self.vehicles[i].len
				if state not in true_cost or true_cost[state] > cost:
					expanded_nodes += 1
					true_cost[state] = cost
					heapq.heappush(frontiers, (cost + self.heuristic(state), state))
					parents[state] = curr_state
		
		return None, None, 0