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
		visited = []
		frontiers = deque([init_state])
		parents = {init_state: None}

		while frontiers:
			current = frontiers.popleft()
			visited.append(current)

			if self.is_goal(current):
				path = []
				while current is not None:
					path.append(current)
					current = parents[current]
				return path[::-1]

			for i, state in self.generate_move(current):
				if state not in visited:
					parents[state] = current
					frontiers.append(state)

		return None

	def dfs(self) -> list[tuple[tuple[int, int]]]:
		visited = []
		frontiers = deque([self.init_state])
		parents = {self.init_state: None}

		while frontiers:
			current = frontiers.pop()
			visited.append(current)

			if self.is_goal(current):
				path = []
				while current is not None:
					path.append(current)
					current = parents[current]
				return path[::-1]

			for i, state in self.generate_move(current):
				if state not in visited:
					parents[state] = current
					frontiers.append(state)

		return []

	def ucs(self) -> list:
		frontiers = [(0, self.init_state)]
		parents = {self.init_state: None}
		true_cost = {self.init_state: 0}

		while frontiers:
			curr_cost, curr_state = heapq.heappop(frontiers)

			if self.is_goal(curr_state):
				path = []
				cost = []
				while curr_state is not None:
					path.append(curr_state)
					cost.append(true_cost[curr_state])
					curr_state = parents[curr_state]
				return path[::-1], cost[::-1]

			for i, state in self.generate_move(curr_state):
				cost = curr_cost + self.vehicles[i].len
				if state not in true_cost or true_cost[state] > cost:
					true_cost[state] = cost
					heapq.heappush(frontiers, (cost, state))
					parents[state] = curr_state
		
		return None
	
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

		
	# def heuristic(self, state: tuple[tuple[int, int]]) -> int:
	# 	'''
	# 	The state has to be pre-validated
	# 	Counts the number of cars blocking the targeted car from reaching the goal
		
	# 	'''

	# 	count = 0

	# 	for idx in range(1, len(self.vehicles)):
	# 		i, j = state[idx]
	# 		target_i, target_j = state[0]
	# 		if self.vehicles[idx].ori == "V":
	# 			if (0 < target_i - i < self.vehicles[idx].len) and (target_j < j):
	# 				count += 1
	# 		else:
	# 			if (target_i == i) and (target_j < j):
	# 				count += 1

	# 	return count

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
		frontiers = [(self.heuristic(self.init_state), self.init_state)]
		parents = {self.init_state: None}
		true_cost = {self.init_state: 0}

		while frontiers:
			curr_cost, curr_state = heapq.heappop(frontiers)

			if self.is_goal(curr_state):
				path = []
				cost = []
				while curr_state is not None:
					path.append(curr_state)
					cost.append(true_cost[curr_state])
					curr_state = parents[curr_state]
				return path[::-1], cost[::-1]

			for i, state in self.generate_move(curr_state):
				cost = true_cost[curr_state] + self.vehicles[i].len
				if state not in true_cost or true_cost[state] > cost:
					true_cost[state] = cost
					heapq.heappush(frontiers, (cost + self.heuristic(state), state))
					parents[state] = curr_state
		
		return None

#from copy import deepcopy
#
#class Vehicle:
#    def __init__(self, id: str, pos: tuple[int, int], orientation: str, length: int):
#        if type(id) is not str:
#            raise TypeError("Vehicle ID must be a string")
#        else:
#            self.id = id
#        
#        if length not in (2, 3):
#            raise ValueError("Vehicle length must be 2 or 3")
#        else: 
#            self.length = length
#        
#        if (pos[0] < 0 or pos[0] >= 6) or (pos[1] < 0 or pos[1] >= 6):
#            raise ValueError("Position must be within the grid (0-5, 0-5)")
#        else:
#            self.pos = pos
#        
#        if orientation not in ("horizontal", "vertical"):
#            raise ValueError("orientation must be 'horizontal' or 'vertical'")
#        else:
#            self.orientation = orientation
#        
#    
#class Board:
#    def __init__(self, vehicles: list[Vehicle], rows=6, cols=6):
#        self.rows = rows
#        self.cols = cols
#        self.vehicles = vehicles
#        self.init_board()
#
#    def init_board(self):
#        self.board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
#        for vehicle in self.vehicles:
#            if vehicle.orientation == "horizontal":
#                for i in range(vehicle.length):
#                    self.board[vehicle.pos[0]][vehicle.pos[1] + i] = vehicle.id
#            else:
#                for i in range(vehicle.length):
#                    self.board[vehicle.pos[0] + i][vehicle.pos[1]] = vehicle.id
#    
#                    
#    def clear_board(self):
#        self.board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
#        
#    def is_finished(self):
#        for vehicle in self.vehicles:
#            if vehicle.id == "X":
#                if vehicle.orientation == "horizontal":
#                    if vehicle.pos[0] == 2 and vehicle.pos[1] + vehicle.length - 1 == 5:
#                        return True
#        return False
#    
#    def copyBoard(self):
#        v = deepcopy(self.vehicles)
#        return Board(v)
#    
#    
#    def move(self, id: str, step=1):
#        if step not in [-1, 1]:
#            raise ValueError("Must take only 1 step at a time")
#        
#        vehicles = deepcopy(self.vehicles)
#        
#        for v in vehicles:
#            if v.id == id:
#                vehicle = v
#                break
#        else:
#            raise ValueError("ID not exist")
#        
#        i, j = vehicle.pos
#
#        if vehicle.orientation == "horizontal":
#            start, end = j, j + vehicle.length
#            if (step == 1) and (end >= self.cols or self.board[i][end] != '.'):
#                return None
#            if (step != 1) and (start <= 0 or self.board[i][start - 1] != '.'):
#                return None
#            
#            vehicle.pos = (i, j + step)
#            
#        else:
#            start, end = i, i + vehicle.length
#            if (step == 1) and (end >= self.rows or self.board[end][j] != '.'):
#                return None
#            if (step != 1) and (start <= 0 or self.board[start - 1][j] != '.'):
#                return None
#            
#            vehicle.pos = (i + step, j)
#
#        return Board(vehicles)
#