def find_all(string, substring):
	indices = list()
	i = -1
	while i < len(string):
		index = string.find(substring, i+1)
		if index > -1:
			indices.append(index)
			i = index
		else:
			break
	return indices

def find_char_sets(string):
	unique_chars = list(set(string))
	unique_chars.remove('*')
	
	char_list = list()
	for char in unique_chars:
		char_list.append(find_all(string, char))
		
	char_dict = dict()
	for char in unique_chars:
		char_dict[char] = char_list
		
	return char_dict, len(char_list)

def get_permutation_list(index_list):
	if len(index_list) <= 1:
		return [index_list]
	
	permutations = list()
	for i in range(0, len(index_list)):
		sub_permutations = get_permutation_list(index_list[:i]+index_list[i+1:])
		for sp in sub_permutations:
			permutations.append([index_list[i]]+sp)
	return permutations

def state_set(state_str):
	state_set = set()

	for i in range(0, len(state_str), 4):
		state_set.add(state_str[i:i+4])
	return state_set

def get_permutations(string):
	char_dict, index_len = find_char_sets(string)
	index_permutations = get_permutation_list(list(range(0, index_len)))

	permutations = list()
	for index_list in index_permutations:
		new_string = '*'*len(string)
		for key in char_dict:
			index = index_list.pop(0)
			index_sets = char_dict[key]
			for loc in index_sets[index]:
				new_string = new_string[:loc]+key+new_string[loc+1:]
		permutations.append(state_set(new_string))
	return permutations