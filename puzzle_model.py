class PuzzleModel:

	def __init__(self, bins):
		self.max_vol = 4

		if type(bins) == dict:
			self.bins = bins
			self.state = self.state_enc()
		else:
			self.bins = self.state_unenc(bins)
			self.state = bins

		self.win_state = self.check_win()
		self.stuck_state = False

	def is_bin_complete(self, b):
		if len(b) != self.max_vol and len(b) != 0:
			return False
		for i in range(1, len(b)):
			if b[i] != b[0]:
				return False
		return True

	def check_win(self):
		for index in self.bins:
			b = self.bins[index]
			if len(b) > 0 and len(b) < self.max_vol:
				return False
			if not self.is_bin_complete(b):
				return False
		return True

	def is_valid_move(self, origin, dest):
		# origin and dest should be integer indices of [bins]

		# check to see if there are any balls in origin:
		if len(self.bins[origin]) <= 0:
			return False
		
		# check to see if there's room in dest
		if len(self.bins[dest]) >= self.max_vol:
			return False
		
		# check to see if last ball in dest is same color as last ball in origin
		# or dest is empty
		if len(self.bins[dest]) > 0 and self.bins[origin][-1] != self.bins[dest][-1]:
			return False
		
		# check to make sure [origin] and [dest] are not equal
		if origin == dest:
			return False
		
		# make sure origin and dest are within bounds
		if origin < 0 or dest < 0 or origin >= len(self.bins) or dest >= len(self.bins):
			return False
		
		# don't allow moves to remove a ball from a completed bin
		if self.is_bin_complete(self.bins[origin]):
			return False
		
		return True

	def process_move(self, move):
		origin = move[0]
		dest = move[1]
		
		new_bins = dict()
		for index in self.bins:
			b = self.bins[index]
			new_bins[index] = b
		new_bins[dest] = new_bins[dest] + new_bins[origin][-1]
		new_bins[origin] = new_bins[origin][0:-1]
		self.bins = new_bins
		self.state = self.state_enc()
		self.win_state = self.check_win()
		options = self.get_options()
		if len(options) > 0:
			self.stuck_state = False
		else:
			self.stuck_state = True
		return new_bins

	def state_enc(self):
		state_str = ''
		for index in self.bins:
			tube = self.bins[index]
			state_str += tube + (self.max_vol-len(tube)) * '*'
		return state_str

	def state_unenc(self, state_str):
		state = dict()
		index = 0
		while len(state_str) > 0:
			tube = state_str[0:4]
			tube = tube.replace('*', '')
			state[index] = tube
			state_str = state_str[4:]
			index += 1
		return state

	def all_one_color(self, tube, color):
		count = 0
		for ball in tube:
			if ball == color:
				count += 1
		if count > 0 and count >= len(tube):
			return True
		return False

	def is_good_move(self, origin, dest):
		# do not move ball if all of the same color won't fit in the dest
		color = self.bins[origin][-1]
		count = 0
		i = len(self.bins[origin]) - 1
		while i >= 0 and self.bins[origin][i] == color:
			count += 1
			i -= 1
		if self.max_vol - len(self.bins[dest]) < count:
			return False
		
		# if ball in origin can be used to finish a tube other than dest, don't move anywhere else
		if not self.all_one_color(self.bins[dest], self.bins[origin][-1]):
			for i in range(0, len(self.bins)):
				if i != origin and i != dest:
					if self.all_one_color(self.bins[i], self.bins[origin][-1]):
						return False
		
		return True

	def get_options(self):
		options = []
		for o in range(0, len(self.bins)):
			for d in range(0, len(self.bins)):
				if self.is_valid_move(o, d) and self.is_good_move(o, d):
					options.append((o, d))
		return options