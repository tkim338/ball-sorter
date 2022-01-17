import networkx as nx
import matplotlib.pyplot as plt

class Graph:
	def __init__(self, data):
		self.graph = nx.Graph()
		self.node_dict = dict()

		index = 0
		for row in data:
			origin_state = row[0]
			action = row[1]
			dest_state = row[2]

			if origin_state not in self.node_dict:
				self.node_dict[origin_state] = index
				index += 1
			if dest_state not in self.node_dict:
				self.node_dict[dest_state] = index
				index += 1

			self.graph.add_edge(self.node_dict[origin_state], self.node_dict[dest_state])
		return

	def show(self):
		nx.draw(self.graph, with_labels=True, font_weight='bold')
		plt.show()
		return

	def print(self):
		for key in self.node_dict:
			print(f'{self.node_dict[key]} = {key}')
		return