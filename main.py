import image_processor
import puzzle_solver

tube_dict = image_processor.process('/Users/tkim/Downloads/bs2.png')
print(tube_dict)

sol = puzzle_solver.solve(tube_dict)
for move in sol:
	print(move)