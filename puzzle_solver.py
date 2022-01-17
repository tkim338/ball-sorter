import random

max_vol = 4

def solve(bins):
	solution = try_options(bins)
	return solution

def is_bin_complete(b):
	if len(b) != max_vol and len(b) != 0:
		return False
	for i in range(1, len(b)):
		if b[i] != b[0]:
			return False
	return True

def check_win(bins):
	for index in bins:
		b = bins[index]
		if len(b) > 0 and len(b) < max_vol:
			return False
		if not is_bin_complete(b):
			return False
	return True

def is_valid_move(bins, origin, dest):
	# origin and dest should be integer indices of [bins]

	# check to see if there are any balls in origin:
	if len(bins[origin]) <= 0:
		return False
	
	# check to see if there's room in dest
	if len(bins[dest]) >= max_vol:
		return False
	
	# check to see if last ball in dest is same color as last ball in origin
	# or dest is empty
	if len(bins[dest]) > 0 and bins[origin][-1] != bins[dest][-1]:
		return False
	
	# check to make sure [origin] and [dest] are not equal
	if origin == dest:
		return False
	
	# make sure origin and dest are within bounds
	if origin < 0 or dest < 0 or origin >= len(bins) or dest >= len(bins):
		return False
	
	# don't allow moves to remove a ball from a completed bin
	if is_bin_complete(bins[origin]):
		return False
	
	return True

def all_one_color(tube, color):
	count = 0
	for ball in tube:
		if ball == color:
			count += 1
	if count > 0 and count >= len(tube):
		return True
	return False

def is_good_move(bins, origin, dest):
	# do not move ball if all of the same color won't fit in the dest
	color = bins[origin][-1]
	count = 0
	i = len(bins[origin]) - 1
	while i >= 0 and bins[origin][i] == color:
		count += 1
		i -= 1
	if max_vol - len(bins[dest]) < count:
		return False
	
	# if ball in origin can be used to finish a tube other than dest, don't move anywhere else
	if not all_one_color(bins[dest], bins[origin][-1]):
		for i in range(0, len(bins)):
			if i != origin and i != dest:
				if all_one_color(bins[i], bins[origin][-1]):
					return False
	
	return True

def get_options(bins):
	options = []
	for o in range(0, len(bins)):
		for d in range(0, len(bins)):
			if is_valid_move(bins, o, d) and is_good_move(bins, o, d):
				options.append((o, d))
				
	# randomize options order
	rand_options = []
	while len(options) > 0:
		i = random.randint(0, len(options)-1)
		rand_options.append(options.pop(i))
	return rand_options

def process_move(bins, move):
	origin = move[0]
	dest = move[1]
	
	new_bins = dict()
	for index in bins:
		b = bins[index]
		new_bins[index] = b
	new_bins[dest] = new_bins[dest] + new_bins[origin][-1]
	new_bins[origin] = new_bins[origin][0:-1]
	return new_bins

def state_enc(state):
	state_str = ''
	for index in state:
		tube = state[index]
		state_str += tube + (max_vol-len(tube)) * '*'
	return state_str

def state_unenc(state_str):
	state = dict()
	index = 0
	while len(state_str) > 0:
		tube = state_str[0:4]
		tube = tube.replace('*', '')
		state[index] = tube
		state_str = state_str[4:]
		index += 1
	return state

def try_options(bins):
	bin_str = state_enc(bins)
	state_dict = {bin_str: []}
	attempted_moves = {bin_str: []}
	
	for i in range(0,100):
		print(f'search depth: {i}')
		new_state_dict = dict()
		
		for state_str in state_dict:
			state = state_unenc(state_str)
			options = get_options(state)
			for option in options:
				# check if move was tried before
				if state_str not in attempted_moves:
					attempted_moves[state_str] = []
				if option not in attempted_moves[state_str]:
					attempted_moves[state_str].append(option)
	
					# check to see if state was reached before
					new_state = process_move(state, option)
					new_state_str = state_enc(new_state)
					if new_state_str not in new_state_dict:
						new_state_dict[new_state_str] = state_dict[state_str] + [option]
						if check_win(new_state):
							return new_state_dict[new_state_str]

		state_dict = dict()
		for new_state_str in new_state_dict:
			state_dict[new_state_str] = new_state_dict[new_state_str]
	return 'solution not found'