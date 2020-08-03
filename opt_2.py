import argparse
import networkx as nx
import algorithm
import graph_utils

parser = argparse.ArgumentParser(description='OPT 1 and OPT 2 library')

parser.add_argument('--input',
                    action='store',
                    type=str,
                    help='input dot file',
                    default='example.dot')

parser.add_argument('--verbose',
                    action='store',
                    type=bool,
                    help='if enable, it will be verbose',
                    default=True)

parser.add_argument('--output',
                    action='store',
                    type=str,
                    help='output dot file',
                    default='output.dot')

args = parser.parse_args()
input_file = args.input
verbose = args.verbose
output_file = args.output

if verbose:
    print("Reading input graph...")

G = nx.nx_agraph.read_dot(input_file)
if verbose:
    nodes, edges, clock = graph_utils.graph_stats(G)
    print(f"The input graph has {nodes} nodes, {edges} edges.")
    print(f"The clock of the input graph is {clock} cycles.")

if verbose:
    print("Starting graph preprocessing...")

G = graph_utils.preprocess(G)
if verbose:
    print("Computing matrix W and D...")

W, D = algorithm.WD(G)
if verbose:
    print("D is:")
    # print(f"{D}")
    print("W is:")
    # print(f"{W}")

if verbose:
    print("Running OPT 2...")
Gr = algorithm.OPT_2(G, D)
nodes, edges, clock = graph_utils.graph_stats(G)
if verbose:
    print(f"OPT 2 COMPLETED.")
    print(f"The OPT 2 optimized graph has {nodes} nodes, {edges} edges.")
print(f"The clock of the OPT 2 optimized graph is {clock} cycles.")

graph_utils.save_graph(Gr, output_file)
print(f"The retimed graph has been saved.")