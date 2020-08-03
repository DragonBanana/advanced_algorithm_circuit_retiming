import copy
import math
import networkx as nx
import numpy as np

import graph_utils


def WD(G: nx.DiGraph):
    # Retrieve all the node delays
    node_delays = np.array([int(G.nodes[node]['d']) for node in G.nodes])
    node_dict = dict(zip(list(G.nodes), list(range(len(node_delays)))))
    node_dict_inv = dict(zip(list(range(len(node_delays))), list(G.nodes)))

    class Weight:
        def __init__(self, w, d):
            self.w = w
            self.d = d

        def __add__(self, other):
            return Weight(self.w + other.w, self.d + other.d)

        def __le__(self, other):
            if self.w < other.w:
                return True
            elif self.w == other.w and self.d > other.d:
                return True
            else:
                return False

        def __str__(self):
            return f"[{self.w}, {self.d}]"

        def __repr__(self):
            return self.__str__()

    A = np.matrix(nx.to_numpy_matrix(G, weight='w', nonedge=np.inf))
    A = A.astype(np.object)

    for u, v in G.edges:
        A[node_dict[u], node_dict[v]] = Weight(G[u][v]['w'], G[u][v]['d'])

    n, m = A.shape

    _edges = set([(node_dict[u], node_dict[v]) for u,v in G.edges])
    for row in range(n):
        for col in range(m):
            if (row, col) not in _edges:
                A[row, col] = Weight(np.inf, np.inf)
            else:
                u = node_dict_inv[row]
                v = node_dict_inv[col]
                A[row, col] = Weight(G[u][v]['w'], G[u][v]['d'])

    n, m = A.shape
    A[np.identity(n) == 1] = Weight(0,0)  # diagonal elements should be zero
    for i in range(n):
        A = np.minimum(A, A[i, :] + A[:, i])

    W = np.empty(shape=A.shape, dtype=int)
    D = np.empty(shape=A.shape, dtype=int)
    for row in range(n):
        for col in range(m):
            W[row, col] = A[row, col].w
            D[row, col] = A[row, col].d

    # Add the starting delay
    for x in range(D.shape[0]):
        D[x] = D[x] + node_delays

    return W, D


def CP(G: nx.DiGraph):

    # Retrieve the edges where w is equal to zero
    relevant_edges = [(u, v) for u, v in G.edges if G.get_edge_data(u, v)['w'] == 0]

    # Create a new graph in order to avoid side effects on the current one
    X = nx.DiGraph()

    # Add only the relevant edges to the new graph
    [X.add_edge(u, v, w=G[u][v]['w']) for u, v in relevant_edges]

    # Topological sort the graph
    sorted_vertices = nx.topological_sort(X)

    # DELTA (as described in the paper)
    delta = {}

    # Compute the starting DELTA for each vertex
    for vertex in G.nodes:
        delta[vertex] = int(G.nodes[vertex]['d'])

    # Declare a function that compute incrementally DELTA
    def compute_delay(G, vertex, delay):
        in_vertices = [u for u, v in G.in_edges(vertex)]
        if len(in_vertices) == 0:
            delta[vertex] = delay
        else:
            delta[vertex] = max(delta[vertex] for vertex in in_vertices) + delay

    # Compute DELTA delay
    [compute_delay(X, vertex, int(G.nodes[vertex]['d'])) for vertex in sorted_vertices]

    # Return DELTA
    return delta


def OPT_1(G: nx.DiGraph, W: np.matrix, D: np.matrix, verbose=False):
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
    binary_search_index = binary_search_step

    # Binary search
    for _ in range(math.ceil(math.log2(binary_search_array.size)) + 1):

        # Check exit condition:
        if binary_search_index >= len(binary_search_array) or binary_search_index < 0:
            break

        # Retrieve a clock and try it if feasible
        c = binary_search_array[binary_search_index]

        if c not in tested_c:
            # c = 10
            # Retrieve the index of the path with delay greater than c
            indices = np.where(D > c, D, 0).nonzero()


            # Create a graph to solve the ILP
            bellman_ford_solver_graph = nx.DiGraph()


            # Add constraints
            for x, y in zip(indices[0], indices[1]):
                u = node_names[x]
                v = node_names[y]
                w = W[x, y] - 1
                # print(f"{x} - {y} <= {w}")
                if bellman_ford_solver_graph.has_edge(v,u):
                    if bellman_ford_solver_graph[v][u]['w'] > w:
                        bellman_ford_solver_graph[v][u]['w'] = w
                else:
                    bellman_ford_solver_graph.add_edge(v, u, w=w)

            # Add constraints
            for nodes, edge_property in G.edges.items():
                u = nodes[0]
                v = nodes[1]
                w = edge_property['w']
                # print(f"{u} - {v} <= {w}")
                if bellman_ford_solver_graph.has_edge(v,u):
                    if bellman_ford_solver_graph[v][u]['w'] > w:
                        bellman_ford_solver_graph[v][u]['w'] = w
                else:
                    bellman_ford_solver_graph.add_edge(v, u, w=w)

            # print(len(G.edges))
            # print(len(indices[0]))
            # print(len(bellman_ford_solver_graph.edges))

            # graph_utils.print_graph(bellman_ford_solver_graph)
            bellman_ford_solver_graph.add_node('root_node')
            for node in G.nodes:
                bellman_ford_solver_graph.add_edge('root_node', node, w=0)
            # break
            # graph_utils.draw_graph(bellman_ford_solver_graph)
            tested_c.add(c)

            # Solve the graph
            is_feasible = True
            try:
                # graph_utils.draw_graph(bellman_ford_solver_graph)
                r = nx.single_source_bellman_ford_path_length(bellman_ford_solver_graph, 'root_node', weight='w')
                # print(r)
            except nx.NetworkXUnbounded:
                is_feasible = False

            if verbose:
                print(f"Clock {c} {'is' if is_feasible else 'is NOT'} feasible")

            if is_feasible:
                if best_c > c:
                    best_c = c
                    best_r = r

        else:
            is_feasible = c >= best_c

        # Move the index
        binary_search_step = binary_search_step / 2
        if is_feasible:
            binary_search_index = binary_search_index - math.ceil(binary_search_step)
        else:
            binary_search_index = binary_search_index + math.ceil(binary_search_step)
    Gr = graph_utils.retime_graph(G, best_r)

    return Gr


def FEAS(G: nx.DiGraph, c: int):
    r = dict(zip(G.nodes, [0 for _ in G.nodes]))

    # Clone the graph
    Gr = copy.deepcopy(G)

    for i in range(len(Gr.nodes) - 1):
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

def OPT_2(G: nx.DiGraph, D: np.matrix, verbose=False):

    tested_c = set([])
    best_c = np.inf

    # Initialize binary search data structure
    binary_search_array = np.array(sorted(D.flat))
    binary_search_array = np.unique(binary_search_array)
    binary_search_step = int(binary_search_array.size / 2)
    binary_search_index = binary_search_step

    Gr = copy.deepcopy(G)

    # Binary search
    for _ in range(math.ceil(math.log2(binary_search_array.size)) + 1):

        # Check exit condition:
        if binary_search_index >= len(binary_search_array) or binary_search_index < 0:
            break

        # Retrieve a clock and try it if feasible
        c = binary_search_array[binary_search_index]

        if c not in tested_c:

            FEAS_result = FEAS(G, c)

            # Solve the graph
            is_feasible = FEAS_result is not None

            if verbose:
                print(f"Clock {c} {'is' if is_feasible else 'is NOT'} feasible")
            tested_c.add(c)

            if is_feasible:
                if best_c > c:
                    best_c = c
                    Gr = FEAS_result

        else:
            is_feasible = c >= best_c

        # Move the index
        binary_search_step = binary_search_step / 2
        if is_feasible:
            binary_search_index = binary_search_index - math.ceil(binary_search_step)
        else:
            binary_search_index = binary_search_index + math.ceil(binary_search_step)


    return Gr