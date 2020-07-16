from random import randint

import networkx as nx

from graph_utils import print_graph


def gen_correlator(n_bit: int,
                   host_delay: int = 0,
                   compare_delay: int = 3,
                   sum_delay: int = 7):
    assert n_bit > 2, "n_bit should be at least 2"

    # Create a directed graph
    G = nx.DiGraph()

    # Host node
    host_node = 'vh'

    # Comparators
    comparator_nodes = [f"vcomp_{i}" for i in range(n_bit)]

    # Sum operators
    sum_nodes = [f"vsum_{i}" for i in range(n_bit - 1)]

    G.add_node(host_node, d=host_delay)
    G.add_nodes_from(comparator_nodes, d=compare_delay)
    G.add_nodes_from(sum_nodes, d=sum_delay)

    # Build the edges
    G.add_edge(host_node, comparator_nodes[0], w=1)
    for u, v in zip(comparator_nodes[:-1], comparator_nodes[1:]):
        G.add_edge(u, v, w=1)

    G.add_edge(comparator_nodes[-1], sum_nodes[0], w=0)
    G.add_edge(sum_nodes[-1], host_node, w=0)
    for u, v in zip(sum_nodes[:-1], sum_nodes[1:]):
        G.add_edge(u, v, w=0)

    for u, v in zip(comparator_nodes[:-1], reversed(sum_nodes)):
        G.add_edge(u, v, w=0)

    return G


def gen_tree(depth: int,
             delay: int = 5,
             n_branch: int = 2,
             random_delays: bool = False):
    assert depth > 0, "depth should be at least 0"

    G = nx.balanced_tree(n_branch, depth).to_directed(as_view=False)
    for node_attribute in G.nodes:
        G.nodes[node_attribute]['d'] = delay if not random_delays else randint(1, delay)

    edge_to_be_removed = []
    for u, v in G.edges:
        if u < v:
            edge_to_be_removed += [(u, v)]
        else:
            G[u][v]['w'] = 0

    G.remove_edges_from(edge_to_be_removed)

    G.add_node('vh', d=0)
    G.add_edge(0, 'vh', w=depth + 1)
    parent_nodes = set([v for u, v in G.in_edges])
    for u in G.nodes:
        if u not in parent_nodes:
            G.add_edge('vh', u, w=0)

    return G


def gen_full_graph(nodes: int,
                   delay: int = 5,
                   random_delays: bool = False):
    assert nodes > 0, "depth should be at least 0"

    G = nx.complete_graph(nodes).to_directed(as_view=False)
    for node_attribute in G.nodes:
        G.nodes[node_attribute]['d'] = delay if not random_delays else randint(1, delay)

    edge_to_be_removed = []
    for u, v in G.edges:
        if u < v:
            edge_to_be_removed += [(u, v)]
        else:
            G[u][v]['w'] = 0

    G.remove_edges_from(edge_to_be_removed)

    G.add_node('vh', d=0)
    G.add_edge(0, 'vh', w=nodes)
    parent_nodes = set([v for u, v in G.in_edges])
    for u in G.nodes:
        if u not in parent_nodes:
            G.add_edge('vh', u, w=0)

    return G
