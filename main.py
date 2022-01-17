import image_processor
import puzzle_solver
from puzzle_model import PuzzleModel 

tube_dict = image_processor.process('/Users/tkim/Downloads/bs3.png')
print(tube_dict)

model = PuzzleModel(tube_dict)
print(model.bins)
print(model.win_state)


sol = puzzle_solver.solve(tube_dict)
for move in sol:
	print(move)

# print(model.get_options())

# # model.process_move((0, 3))
# # model.process_move((0, 3))
# # model.process_move((0, 4))
# # model.process_move((1, 4))
# # model.process_move((1, 0))
# # model.process_move((2, 3))
# # model.process_move((2, 4))
# # model.process_move((2, 0))
# # model.process_move((1, 4))
# # model.process_move((2, 3))
# # model.process_move((1, 0))

# print(model.bins)
# print(model.state)
# print(model.win_state)