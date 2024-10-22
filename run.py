import argparse
import networkx as nx
import algorithm
import gen_circuits
import graph_utils
import numpy as np
parser = argparse.ArgumentParser(description='OPT 1 and OPT 2 library')

parser.add_argument('--input',
                    action='store',
                    type=str,
                    help='input dot file',
                    default='dot/run_1000')

parser.add_argument('--verbose',
                    action='store',
                    type=bool,
                    help='if enable, it will be verbose',
                    default=True)

args = parser.parse_args()
input_file = args.input
verbose = args.verbose

if verbose:
    print("Reading input graph...")

G = nx.nx_agraph.read_dot(input_file)
# G = gen_circuits.gen_correlator(30)
G = graph_utils.preprocess(G)
if verbose:
    nodes, edges, clock = graph_utils.graph_stats(G)
    print(f"The input graph has {nodes} nodes, {edges} edges.")
    print(f"The clock of the input graph is {clock} cycles.")
if verbose:
    print("Starting graph preprocessing...")
if verbose:
    print("Computing matrix W and D...")

W, D = algorithm.WD(G)
if verbose:
    print("D is:")
    print(f"{D}")
    print("W is:")
    print(f"{W}")

if verbose:
    print("Running OPT 1...")
Gr = algorithm.OPT_1(G, W, D, verbose=verbose)
nodes, edges, clock = graph_utils.graph_stats(Gr)
if verbose:
    print(f"OPT 1 COMPLETED.")
    print(f"The OPT 1 optimized graph has {nodes} nodes, {edges} edges.")
print(f"The clock of the OPT 1 optimized graph is {clock} cycles.")

Gr = algorithm.OPT_2(G, D, verbose=verbose)
nodes, edges, clock = graph_utils.graph_stats(Gr)
if verbose:
    print(f"OPT 2 COMPLETED.")
    print(f"The OPT 2 optimized graph has {nodes} nodes, {edges} edges.")
print(f"The clock of the OPT 2 optimized graph is {clock} cycles.")