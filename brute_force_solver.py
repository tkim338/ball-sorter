import image_processor
from puzzle_model import PuzzleModel
import sys
import random

def equal_states(state0, state1):
	return True

def solve(model):
	bin_str = model.state
	state_dict = {bin_str: []}
	attempted_moves = {bin_str: []}
	
	for i in range(0,1000):
		print(f'search depth: {i}')
		new_state_dict = dict()
		
		for state_str in state_dict:
			parent_model = PuzzleModel(state_str)
			options = parent_model.get_options()
			for option in options:
				# check if move was tried before
				if state_str not in attempted_moves:
					attempted_moves[state_str] = []
				if option not in attempted_moves[state_str]:
					attempted_moves[state_str].append(option)
	
					# check to see if state was reached before
					option_model = PuzzleModel(parent_model.state)
					option_model.process_move(option)

					if option_model.state not in new_state_dict:
						new_state_dict[option_model.state] = state_dict[state_str] + [option]
						if option_model.win_state:
							return new_state_dict[option_model.state]

		state_dict = dict()
		for new_state_str in new_state_dict:
			state_dict[new_state_str] = new_state_dict[new_state_str]

	return 'solution not found'

if __name__ == "__main__":
	print(sys.argv[1])
	image_loc = sys.argv[1]
	tube_dict = image_processor.process(image_loc)
	model = PuzzleModel(tube_dict)
	print(model.bins)
	print(model.win_state)

	# print(model.to_string())
	sol = solve(model)
	for move in sol:
		print(move)