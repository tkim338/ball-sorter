import image_processor
from puzzle_model import PuzzleModel
import sys
import random

def dfs_search(model, state_history, path):
	# state_history = [model.state_set()]
	for i in range(0,100):
		print(f'Path length: {len(path)}. Paths checked: {i}.')

		if model.state_set() not in state_history:
			state_history.append(model.state_set())
			options = model.get_options()
			for option in options:
				# attempt option
				option_model = PuzzleModel(model.state)
				option_model.process_move(option)
				if option_model.win_state == True:
					return True, state_history, path+[option]
				else:
					won, state_history, p = dfs_search(option_model, state_history, path+[option])
					if won:
						return True, state_history, p
			# no options for this model
		# model state set already checked
	# path limit reached
	return False, state_history, path

if __name__ == "__main__":
	image_loc = sys.argv[1]
	tube_dict = image_processor.process(image_loc)
	model = PuzzleModel(tube_dict)
	# print(model.bins)
	# print(model.win_state)

	print(model.to_string())
	win_state, history, sol = dfs_search(model, list(), list())
	for move in sol:
		print(f'{move[0]+1}, {move[1]+1}')