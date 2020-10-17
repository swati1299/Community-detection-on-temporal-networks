import matplotlib.pyplot as plt
import networkx as nx

# matplotlib version 2.2.3 is required
# making graph1 and community 1
text_file = open("results\\10001000150.70.80.31\\graph-1.txt", "r")
src = list()
for line in text_file:
    src.append([int(x) for x in line.split('\t')])

text_file.close()
# print(src)

G = nx.Graph()
for edges in src:
    ed = (edges[0], edges[1])
    G.add_edge(*ed)
'''
nx.draw(G,with_labels=True)
plt.draw()
#plt.show()
'''
# ---------------------- this was till normal graph plotting -----------------------------------------------
# ------------------------ now we'll show communities --------------------------------------------

file = open("results\\10001000150.70.80.31\\communities-1.txt", "r")
node_groups = []
for line in file:
    node_groups.append([int(x) for x in line.split(',')])

file.close()
# print(node_groups)
color_map = []
colors = ['blue', 'green', 'yellow', 'cyan', 'red', 'magenta']

# range(66) is because graph-1 has 66 communities in total

for node in G:
    for i in range(66):
        if node in node_groups[i]:
            color_map.append(colors[i % 6])
nx.draw(G, node_color=color_map)
plt.show()

