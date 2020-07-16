import functools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import memory_profiler
import algorithm
import graph_utils
import gen_circuits

path = "graph.dot"

root_node = 'root_node'

# G = nx.nx_agraph.read_dot(path)

# G = graph_utils.preprocess(G)

G = gen_circuits.gen_correlator(4)
# G = gen_circuits.gen_tree(depth=3, n_branch=3, random_delays=True)
# G = gen_circuits.gen_full_graph(100, random_delays=True)

G = graph_utils.preprocess(G)
W, D = algorithm.WD(G)

Gr = algorithm.OPT_1(G, W, D)
# Gr = algorithm.OPT_2(G, D)

# graph_utils.print_graph(Gr)

print(algorithm.CP(G))
print(max(algorithm.CP(G).values()))
print(algorithm.CP(Gr))
print(max(algorithm.CP(Gr).values()))

graph_utils.draw_graph(G)
graph_utils.draw_graph(Gr)

# G = gen_circuits.gen_full_graph(10)
# graph_utils.print_graph(G)
# graph_utils.draw_graph(G)

# f = functools.partial(algorithm.OPT_1, G=G, W=W, D=D)
# mem_usage = memory_profiler.memory_usage(f, timestamps=True)
# print(mem_usage)
# print(min(mem_usage))
# print(max(mem_usage))