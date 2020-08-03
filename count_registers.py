import os
from random import randint
import networkx as nx
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import algorithm
import graph_utils

n_graphs = 1000
n_nodes = 25
k_out = 15
max_delay = 10000
count_file = open("count_registers.csv", 'w+')
count_file.write("filename, nodes, edges, opt_1 registers, opt_2 registers\n")
count_file.flush()
if not os.path.exists("dot"):
    os.mkdir("dot")

def gen_graph(random_seed):
    template = nx.generators.directed.random_k_out_graph(n=n_nodes, k=k_out, alpha=0.5, self_loops=False, seed=17)
    graph_0 = nx.DiGraph()
    graph_1 = nx.DiGraph()
    for node in template.nodes:
        graph_0.add_node(node, d=randint(1, max_delay))
        graph_1.add_node(node, d=randint(1, max_delay))
    for edge in template.edges:
        u, v, _ = edge
        if randint(0, 5) < 1:
            graph_0.add_edge(u, v, w=0)
        else:
            graph_1.add_edge(u, v, w=1)
    while True:
        try:
            cycle_edges = nx.find_cycle(graph_0)
        except:
            break
        for edge in cycle_edges:
            u, v = edge
            graph_0.remove_edge(u, v)
            graph_1.add_edge(u, v , w=1)
    for edge in graph_0.edges:
        u, v = edge
        graph_1.add_edge(u, v, w=0)

    for node in graph_1.nodes:
        desc = nx.descendants(graph_1, node)
        for n in graph_1.nodes:
            if n not in desc and n != node :
                graph_1.add_edge(node, n, w=1)

    graph_utils.save_graph(graph_1, f"dot/run_{random_seed+1000}")

def count_registers(G):
    return sum([G.get_edge_data(*edge)['w'] for edge in G.edges])

def calc_graph(random_seed):
    path = f"dot/run_{random_seed+1000}"
    G = nx.nx_agraph.read_dot(path)
    G = graph_utils.preprocess(G)
    W, D = algorithm.WD(G)
    Gr = algorithm.OPT_1(G, W, D)
    count_1 = count_registers(Gr)
    clock_1 = max(algorithm.CP(Gr).values())
    Gr = algorithm.OPT_2(G, D)
    count_2 = count_registers(Gr)
    clock_2 = max(algorithm.CP(Gr).values())
    nodes, edges, clock = graph_utils.graph_stats(Gr)
    # assert clock_1 == clock_2, f"{clock_1}, {clock_2}, {random_seed}"
    count_file.write(f"{path}, {nodes}, {edges}, {count_1}, {count_2}\n")
    count_file.flush()

# process_map(gen_graph, list(range(n_graphs)), max_workers=8)
process_map(calc_graph, list(range(n_graphs)), max_workers=8)