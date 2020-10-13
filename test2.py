# based loosely on https://amunategui.github.io/reinforcement-learning/index.html
# and https://www.redblobgames.com/pathfinding/grids/graphs.html

import numpy as np
import pylab as plt

all_nodes = []
for x in range(10):
    for y in range(5):
        all_nodes.append([x, y])

import networkx as nx
G=nx.Graph()
G.add_edges_from(all_nodes)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos)
plt.show()

def neighbors(node):
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    result = []
    for dir in dirs:
        neighbor = [node[0] + dir[0], node[1] + dir[1]]
        if neighbor in all_nodes:
            result.append(neighbor)
    return result

