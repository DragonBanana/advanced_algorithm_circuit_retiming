import copy

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import algorithm


def preprocess(G: nx.DiGraph):

    # Clone graph G
    G = copy.deepcopy(G)

    # Preprocess the data
    for edge_key, edge_property in G.edges.items():
        u = edge_key[0]
        v = edge_key[1]
        w = int(edge_property['w'])
        d = int(G.nodes[u]['d'])
        G[u][v]['w'] = w
        G[u][v]['d'] = d

    return G

def retime_graph(G: nx.DiGraph, r):

    # Clone the graph
    Gr = copy.deepcopy(G)
    # Move the registers
    for u, v in list(G.edges):
        Gr[u][v]['w'] = G[u][v]['w'] + r[v] - r[u]

    # Return the new graph
    return Gr

def print_graph(G: nx.DiGraph):
    # Move the registers
    for u, v in sorted(list(G.edges)):
        print(f"[{u}] -- {G[u][v]['w']} --> [{v}] ")


def draw_graph(G: nx.DiGraph):
    nx.draw(G, pos=nx.circular_layout(G), with_labels=True)
    nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G))
    plt.show()


def save_graph(G, filename="example.dot"):
    nx.nx_agraph.write_dot(G, filename)

def graph_stats(G):
    n_nodes = len(G.nodes)
    n_edges = len(G.edges)
    f_clock = max(algorithm.CP(G).values())
    return n_nodes, n_edges, f_clock