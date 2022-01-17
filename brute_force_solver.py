import image_processor
import puzzle_solver
from puzzle_model import PuzzleModel
import sys

if __name__ == "__main__":
	print(sys.argv[1])
	image_loc = sys.argv[1]
	tube_dict = image_processor.process(image_loc)
	model = PuzzleModel(tube_dict)
	print(model.bins)
	print(model.win_state)

	sol = puzzle_solver.solve(tube_dict)
	for move in sol:
		print(move)