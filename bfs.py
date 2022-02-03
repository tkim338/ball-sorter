import image_processor
from puzzle_model import PuzzleModel
import sys
import random

def solve(model):
	state_history = [model.state_set()]

	bin_str = model.state
	state_dict = {bin_str: []}
	attempted_moves = {bin_str: []}
	
	for i in range(0,1000):
		print(f'search depth: {i}. Trying {len(state_dict.keys())} states.')
		new_state_dict = dict()
		
		state_str_to_remove = list()
		for state_str in state_dict:
			parent_model = PuzzleModel(state_str)
			options = parent_model.get_options()

			has_path = False

			for option in options:
				# check if move was tried before
				if state_str not in attempted_moves:
					attempted_moves[state_str] = []
				if option not in attempted_moves[state_str]:
					# try this option
					attempted_moves[state_str].append(option)
	
					# check to see if state was reached before
					option_model = PuzzleModel(parent_model.state)
					option_model.process_move(option)

					# if option_model.state not in state_dict and option_model.state not in new_state_dict:
					if option_model.state_set() not in state_history:
						has_path = True
						# state_history.append(option_model.state)
						state_history.append(option_model.state_set())

						new_state_dict[option_model.state] = state_dict[parent_model.state] + [option]
						if option_model.win_state:
							with open('outputs/history.txt', 'w') as f:
								f.write(str(state_history))
								f.close()
							return new_state_dict[option_model.state]

			if has_path == False:
				state_str_to_remove.append(state_str)

		for state_to_remove in state_str_to_remove:
			state_dict.pop(state_to_remove, None)
		for new_state_str in new_state_dict:
			state_dict[new_state_str] = new_state_dict[new_state_str]

	return 'solution not found'

if __name__ == "__main__":
	image_loc = sys.argv[1]
	tube_dict = image_processor.process(image_loc)
	model = PuzzleModel(tube_dict)
	# print(model.bins)
	# print(model.win_state)

	print(model.to_string())
	sol = solve(model)
	for move in sol:
		print(f'{move[0]+1}, {move[1]+1}')