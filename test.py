import time

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import algorithm
import graph_utils
import gen_circuits

def test_graph(G: nx.DiGraph, expected_clock):
    W, D = algorithm.WD(G)
    # Using OPT 1
    time_1 = time.time()
    Gr_1 = algorithm.OPT_1(G, W, D)
    time_1 = time.time() - time_1
    # Using OPT 2
    time_2 = time.time()
    Gr_2 = algorithm.OPT_2(G, D)
    time_2 = time.time() - time_2

    # Check
    n_nodes_1, n_edges_1, f_clock_1 = graph_utils.graph_stats(Gr_1)
    # Check
    n_nodes_2, n_edges_2, f_clock_2 = graph_utils.graph_stats(Gr_2)

    assert f_clock_1 == f_clock_2, f"The clock of OPT_1 ({f_clock_1}) is not equal to the clock of OPT_2 ({f_clock_2})."
    assert f_clock_1 == expected_clock, f"The clock ({f_clock_1}) is not equal to the expected one ({expected_clock})."

    return n_nodes_1, n_edges_1, f_clock_1, time_1, time_2


file = open("test_result.csv", "w+")

# Test the correlator
for i in range(6, 50):
    G = gen_circuits.gen_correlator(i)
    G = graph_utils.preprocess(G)
    print(i)
    nodes, edges, clock, t_1, t_2 = test_graph(G, 14)
    file.write(f"Correlator {i} bit, {nodes}, {edges}, {clock}, {t_1}, {t_2}\n")
    file.flush()

# Test the correlator
for i in range(10, 500, 5):
    G = gen_circuits.gen_full_graph(i)
    G = graph_utils.preprocess(G)
    nodes, edges, clock, t_1, t_2 = test_graph(G, 5)
    file.write(f"Full graph {i} nodes, {nodes}, {edges}, {clock}, {t_1}, {t_2}\n")
    file.flush()

# Test the correlator
for i in range(1, 8):
    for j in range(1, 8):
        G = gen_circuits.gen_tree(n_branch=i, depth=j)
        G = graph_utils.preprocess(G)
        nodes, edges, clock, t_1, t_2 = test_graph(G, 5)
        file.write(f"Tree n_branch {i} depth {j}, {nodes}, {edges}, {clock}, {t_1}, {t_2}\n")
        file.flush()