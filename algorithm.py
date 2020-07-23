import math

import networkx as nx
import numpy as np

import graph_utils


def WD(G: nx.DiGraph):
    node_delays = np.array([int(G.nodes[node]['d']) for node in G.nodes])

    W = nx.floyd_warshall_numpy(G, weight='w').astype(int)
    D = nx.floyd_warshall_numpy(G, weight='d').astype(int)

    for x in range(D.shape[0]):
        D[x] = D[x] + node_delays

    return W, D


def CP(G: nx.DiGraph):
    relevant_edges = [(u, v) for u, v in G.edges if G.get_edge_data(u, v)['w'] == 0]

    X = nx.DiGraph()

    [X.add_edge(u, v, w=G[u][v]['w']) for u, v in relevant_edges]

    sorted_vertices = nx.topological_sort(X)

    delta = {}
    for vertex in G.nodes:
        delta[vertex] = int(G.nodes[vertex]['d'])

    def compute_delay(G, vertex, delay):
        in_vertices = [u for u, v in G.in_edges(vertex)]
        if len(in_vertices) == 0:
            delta[vertex] = delay
        else:
            delta[vertex] = max(delta[vertex] for vertex in in_vertices) + delay

    [compute_delay(X, vertex, int(G.nodes[vertex]['d'])) for vertex in sorted_vertices]

    return delta


def OPT_1(G: nx.DiGraph, W: np.matrix, D: np.matrix):
    # Initiliaze returned value
    r = {}
    best_r = {}
    best_c = np.inf

    # Auxiliary structures
    node_names = np.array(G.nodes, np.object)
    tested_c = set([])

    # Initialize binary search data structure
    binary_search_array = np.array(sorted(D.flat))
    binary_search_array = np.unique(binary_search_array)
    binary_search_step = int(binary_search_array.size / 2)
    binary_search_index = binary_search_array.size - binary_search_step

    # Binary search
    while binary_search_step >= 0.1:

        # Retrieve a clock and try it if feasible
        c = binary_search_array[binary_search_index]

        # Retrieve the index of the path with delay greater than c
        indices = np.where(D > c, D, 0).nonzero()

        # Create a graph to solve the ILP
        bellman_ford_solver_graph = nx.DiGraph()

        # Populate the graph
        for nodes, edge_property in G.edges.items():
            u = nodes[0]
            v = nodes[1]
            w = edge_property['w']
            bellman_ford_solver_graph.add_edge(v, u, weight=w)

        for x, y in zip(indices[0], indices[1]):
            u = node_names[x]
            v = node_names[y]
            w = W[x, y] - 1
            bellman_ford_solver_graph.add_edge(v, u, weight=w)

        for node in node_names:
            bellman_ford_solver_graph.add_edge('root_node', node, weight=0)

        # Solve the graph
        is_feasible = True
        for node in node_names:
            try:
                r[node] = nx.bellman_ford_path_length(bellman_ford_solver_graph, source='root_node', target=node)
                if best_c > c:
                    best_c = c
                    best_r = r
            except nx.NetworkXUnbounded:
                is_feasible = False


        tested_c.add(c)

        # if is_feasible:
        #     print(f"Algo OPT 1: clock {c} is feasible")
        # else:
        #     print(f"Algo OPT 1: clock {c} is NOT feasible")
        # print(f"current step -> {binary_search_step}")


        # Move the index
        if binary_search_array[binary_search_index] in tested_c and binary_search_step >= 0.1:
            binary_search_step = binary_search_step / 2
            if is_feasible:
                binary_search_index = binary_search_index - math.ceil(binary_search_step)
            else:
                binary_search_index = binary_search_index + math.ceil(binary_search_step)

    # print(f"last step -> {binary_search_step}")
    Gr = graph_utils.retime_graph(G, best_r)
    
    return Gr


def FEAS(G: nx.DiGraph, c: int):
    r = dict(zip(G.nodes, [0 for _ in G.nodes]))

    # Clone the graph
    Gr = G.copy()

    for _ in range(len(Gr.nodes) - 1):
        path = CP(Gr)
        for node in Gr.nodes:
            if path.get(node, 0) > c:
                r[node] = r[node] + 1
        # Move the registers
        for u, v in list(Gr.edges):
            Gr[u][v]['w'] = G[u][v]['w'] + r[v] - r[u]

    if max(CP(Gr).values()) > c:
        return None
    else:
        return Gr

def OPT_2(G: nx.DiGraph, D: np.matrix):

    tested_c = set([])
    best_c = np.inf

    # Initialize binary search data structure
    binary_search_array = np.array(sorted(D.flat))
    binary_search_array = np.unique(binary_search_array)
    binary_search_step = int(binary_search_array.size / 2)
    binary_search_index = binary_search_step

    Gr = G

    # Binary search
    while binary_search_step >= 0.1:

        # Retrieve a clock and try it if feasible
        c = binary_search_array[binary_search_index]

        FEAS_result = FEAS(G, c)

        # Solve the graph
        is_feasible = FEAS_result is not None

        tested_c.add(c)

        if is_feasible:
            if best_c > c:
                best_c = c
                Gr = FEAS_result

        # Move the index
        while binary_search_array[binary_search_index] in tested_c and binary_search_step >= 0.1:
            binary_search_step = binary_search_step / 2
            if is_feasible:
                binary_search_index = binary_search_index - math.ceil(binary_search_step)
            else:
                binary_search_index = binary_search_index + math.ceil(binary_search_step)

        # if is_feasible:
        #     print(f"Algo OPT 1: clock {c} is feasible")
        # else:
        #     print(f"Algo OPT 1: clock {c} is NOT feasible")
        # print(f"current step -> {binary_search_step}")

    return Gr