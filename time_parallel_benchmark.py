import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm.contrib.concurrent import process_map

import algorithm
import graph_utils
import gen_circuits

file = open("result.csv", "w+")

n_runs = 20

def dispatcher(args):
    return single_run(args[0], args[1])

def opt_1(G):
    time_1 = time.time()
    W, D = algorithm.WD(G)
    Gr_1 = algorithm.OPT_1(G, W, D)
    return time.time() - time_1

def opt_2(G):
    time_2 = time.time()
    W, D = algorithm.WD(G)
    Gr_2 = algorithm.OPT_2(G, D)
    return time.time() - time_2


def single_run(G, run_name):
    # Using OPT 1
    time_1 = [opt_1(G) for _ in range(n_runs)]
    m_time_1 = np.mean(time_1)
    d_time_1 = np.std(time_1)
    # Using OPT 2
    time_2 = [opt_2(G) for _ in range(n_runs)]
    m_time_2 = np.mean(time_2)
    d_time_2 = np.std(time_2)

    # Check
    nodes, edges, clock = graph_utils.graph_stats(G)

    file.write(f"{run_name}, {nodes}, {edges}, {m_time_1}, {d_time_1}, {m_time_2}, {d_time_2}\n")
    file.flush()

runs = []

# Test the correlator
for i in range(2, 5):
    for j in range(1, 5):
        G = gen_circuits.gen_tree(n_branch=i, depth=j)
        G = graph_utils.preprocess(G)
        runs += [(G, f"Tree n_branch {i} depth {j}")]

# Test the correlator
for i in range(2, 5):
    for j in range(1, 5):
        G = gen_circuits.gen_tree(n_branch=i, depth=j, delay=100, random_delays=True)
        G = graph_utils.preprocess(G)
        runs += [(G, f"Tree n_branch {i} depth {j} random_delays")]

# Test the correlator
for j in range(50, 300, 50):
    G = gen_circuits.gen_tree(n_branch=1, depth=j)
    G = graph_utils.preprocess(G)
    runs += [(G, f"Tree n_branch {1} depth {j}")]

# Test the correlator
for j in range(20, 200, 20):
    G = gen_circuits.gen_tree(n_branch=1, depth=j, delay=100, random_delays=True)
    G = graph_utils.preprocess(G)
    runs += [(G, f"Tree n_branch {1} depth {j} random_delays")]

# Test the correlator
for i in range(5, 40, 5):
    G = gen_circuits.gen_correlator(i)
    G = graph_utils.preprocess(G)
    runs += [(G, f"Correlator {i} bit")]

# Test the correlator
for i in range(20, 200, 20):
    G = gen_circuits.gen_full_graph(i)
    G = graph_utils.preprocess(G)
    runs += [(G, f"Full graph {i} nodes")]

# Test the correlator
for i in range(20, 200, 20):
    G = gen_circuits.gen_full_graph(i, delay=100, random_delays=True)
    G = graph_utils.preprocess(G)
    runs += [(G, f"Full graph {i} nodes random_delays")]

process_map(dispatcher, runs, max_workers=20)