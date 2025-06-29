from .gameClass import Vehicle, Board

class Problem:
	init_state = ()
	vehicles_info = []

	def __init__(self, board: Board):
		for vehicle in board.vehicles:
			self.init_state = self.init_state + (vehicle.pos,)
			self.vehicles_info.append([vehicle.id, vehicle.length, vehicle.orientation])

	def is_goal(state: tuple[tuple[int, int]]) -> bool:
		return state[0][1] == 4
	
	def generate_move(self, state: tuple[tuple[int, int]]):
		generated_state = ()

		for pos, vehicle in zip(state, self.vehicles_info):
			pass

		return generated_state