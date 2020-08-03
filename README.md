# Advanced Algorithm Circuit Retiming Project
<p align="center">
  <img width="100%" src="https://i.imgur.com/tm9mSuM.png"/>
</p>
<p align="center">
  <a href="http://recsys.deib.polimi.it">
    <img src="https://i.imgur.com/mPb3Qbd.gif" width="180" />
  </a>
</p>

# Index
* [Introduction](#Introduction)
* [Algorithms](#Algorithms)
* [Documentation](#Documentation)
* [Testing](#Testing)
* [Benchmark](#Benchmark)

# Introduction
[Retiming](https://www.wikiwand.com/en/Retiming) is the technique of moving the structural location of latches or registers in a digital circuit to improve its 
performance, area, and/or power characteristics in such a way that preserves its functional behavior at its outputs. 
Retiming was first described by Charles E. Leiserson and James B. Saxe in 1983.
The technique uses a directed graph where the vertices represent asynchronous combinational blocks and the directed 
edges represent a series of registers or latches (the number of registers or latches can be zero). 
Each vertex has a value corresponding to the delay through the combinational circuit it represents. 
After doing this, one can attempt to optimize the circuit by pushing registers from output to input and vice versa - 
much like bubble pushing. Two operations can be used - deleting a register from each input of a vertex while adding 
a register to all outputs, and conversely adding a register to each input of vertex and deleting a register from all 
outputs. In all cases, if the rules are followed, the circuit will have the same functional behavior 
as it did before retiming.

# Algorithms 
This repository contains a collection of scripts that implements two algorithm: **OPT_1** and **OPT_2**. Both the algorithms are described
in this [paper](https://cseweb.ucsd.edu/classes/sp17/cse140-a/exam/LeisersonRetiming.pdf).
Given a Graph with V vertices and E edges, the complexity of OPT_1 is **O(|V|^3 * lg|V|)** and the
complexity of OPT_2 is **O(|V| \* |E| \* lg|V|)**. So whenever *|E| < |V|^2*, the second algorithm is expected
to eventually have better performance.

### Run the algorithms
In order to run the algorithms use the following scripts:
```shell script
python3 opt1.py --input example.dot --output retimed_example.dot --verbose True
python3 opt2.py --input example.dot --output retimed_example.dot --verbose True
```
# Documentation
The implementation of circuit retiming has been done in Python.

## Requirements
In order to run the code it is necessary to have:
* **Python**: version 3.8. 
* **Pip**: version 20.1.1.

If you do not have Python already installed, you can find it here: https://www.python.org/downloads/.

Install the python dependecies with the following bash command:
```shell script
pip install -r requirements.txt
```
This repository uses the following libraries:
* **numpy**, to handle arrays and matrixes.
* **networkx**, to handle graphs.
* **pygraphviz**, to view graphs.
* **matplotlib**, to plot graphs.
* **memory_profiler**, to profile the memory usage.
* **tqdm**, to monitor *for loops* and *multiprocess tasks*.
* **pandas**, to handle csv results.
* **plotly**, to plot the results in nice charts.

## gen_circuits.py:
The [gen_circuits.py](gen_circuits.py) script contains the functions to generate different types of circuits:
* N bit correlator.
    ```python
    import gen_circuits
    G = gen_circuits.gen_correlator(4)
    ```
    <p align="center">
      <img width="66%" src="doc/images/correlator_4_bit.png"/>
    </p>
* Tree with B branches and D depth.
    ```python
    import gen_circuits
    G = gen_circuits.gen_tree(depth=2, n_branch=2)
    ```
    <p align="center">
      <img width="66%" src="doc/images/bin_tree_2_level.png"/>
    </p>
* Close to fully connected graph with N nodes.
    ```python
    import gen_circuits
    G = gen_circuits.gen_tree(nodes=4)
    ```
    <p align="center">
      <img width="66%" src="doc/images/full_graph_4_node.png"/>
    </p>
For most of the circuits is possible to choose randomize the delay of each node.

To read a custom dot file it is possible to use the *read_dot* feature provided by the NetworkX library.
An example of how the dot file should be formatted can be found [here](example.dot)
```python
import networkx as nx
path = "example.dot"
G = nx.nx_agraph.read_dot(path)
```



## algorithm.py:
The [algorithm.py](algorithm.py) script contains the implementation of 5 algorithms described by Charles E. Leiserson and James B. Saxe.
* **CP**: Given a graph G, for each vertex V, it returns the maximum cost path without registers.
```python
import algorithm, gen_circuits
G = gen_circuits.gen_correlator(4)
X = algorithm.CP(G)
# RESULT
# X: {'vh': 24, 'vcomp_0': 3, 'vcomp_1': 3, 'vcomp_2': 3, 'vcomp_3': 3, 'vsum_0': 10, 'vsum_1': 17, 'vsum_2': 24}
```

* **WD**: Given a graph G, it uses Floyd-Warshall algorithm to build the W and D matrixes described in the paper.
```python
import algorithm, gen_circuits
G = gen_circuits.gen_correlator(4)
W, D = algorithm.WD(G)
# RESULT
# W: matrix([[0, 1, 2, 3, 4, 3, 2, 1],
#            [0, 0, 1, 2, 3, 2, 1, 0],
#            [0, 1, 0, 1, 2, 1, 0, 0],
#            [0, 1, 2, 0, 1, 0, 0, 0],
#            [0, 1, 2, 3, 0, 0, 0, 0],
#            [0, 1, 2, 3, 4, 0, 0, 0],
#            [0, 1, 2, 3, 4, 3, 0, 0],
#            [0, 1, 2, 3, 4, 3, 2, 0]])
```

* **OPT_1**: Given a graph G, a matrix W and a matrix D. It returns a retimed graph with minimum legal clock.
```python
import algorithm, gen_circuits
G = gen_circuits.gen_correlator(4)
W, D = algorithm.WD(G)
retimed_G = algorithm.OPT_1(G, W, D)
```

* **FEAS**: Given a graph G and a clock C, it returns a retimed graph with legal clock C if feasible. Otherwise None.
```python
import algorithm, gen_circuits
G = gen_circuits.gen_correlator(4)
retimed_G = algorithm.FEAS(G, 14)
```

* **OPT_2**: Given a graph G and a matrix D. It returns a retimed graph with minimum legal clock.
```python
import algorithm, gen_circuits
G = gen_circuits.gen_correlator(4)
W, D = algorithm.WD(G)
retimed_G = algorithm.OPT_1(G, D)
```

# Testing
The testing part of the project has been done using the circuits generated with _gen_circuits.py_. Furthermore, OPT_1 
and OPT_2 best clock results are compared and it is checked that they are equal.
The script responsible for the testing is [test.py](test.py).

* **Correlator N bit**:
Given a correlator circuit we know that a minimum clock retiming period of 14 is always possible.

* **Tree with B branches and D depth**:
Given a tree with B branches and D depth, we know that the minimum achievable clock is max(nodes_delay).

* **Graph N nodes**:
Given a graph with N nodes half connected, we know that the clock is max(nodes_delay).
This result is obtained by having a register in each edge of the graph.

# Benchmark
This section contains the benchmark of the two algorithms. It is composed by two subsections: the first one
is related to the time needed to compute the minimum clock and the second one reports the memory consumed.

Those benchmarks have been run on a Intel Xeon 2670 CPU.

## Time benchmark
The script [time_parallel_benchmark.py](time_parallel_benchmark.py) runs OPT_1 and OPT_2 on different circuits.
For each circuit, the algorithm is run **20 times** in order to have a more stable result.
Before running the benchmark we expect that eventually circuits that have **E (Edges) < V^2 (Vertices)** performs better
with OPT_2 rather than with OPT_1.

#### Correlator data
|Circuit name     |Vertices|Edges|Opt 1 time       |Opt 2 time       |
|-----------------|--------|-----|-----------------|-----------------|
|Correlator 5 bit |10      |14   |0.063            |0.018            |
|Correlator 10 bit|20      |29   |0.738            |0.077            |
|Correlator 15 bit|30      |44   |4.600            |0.347            |
|Correlator 20 bit|40      |59   |14.479           |0.673            |
|Correlator 25 bit|50      |74   |39.165           |0.556            |
|Correlator 30 bit|60      |89   |75.612           |0.819            |
|Correlator 35 bit|70      |104  |125.030          |1.057            |

#### Tree data
N branches = 1 (so it is a list of vertices having 1 input edge and 1 output edge).

|Circuit name     |Vertices|Edges|Opt 1 time       |Opt 2 time       |
|-----------------|--------|-----|-----------------|-----------------|
|Tree n_branch 1 depth 20 random_delays|22      |22   |0.302            |0.122            |
|Tree n_branch 1 depth 40 random_delays|42      |42   |3.787            |0.954            |
|Tree n_branch 1 depth 60 random_delays|62      |62   |9.948            |2.192            |
|Tree n_branch 1 depth 80 random_delays|82      |82   |12.408           |2.116            |
|Tree n_branch 1 depth 100 random_delays|102     |102  |41.434           |3.556            |
|Tree n_branch 1 depth 120 random_delays|122     |122  |48.470           |9.729            |
|Tree n_branch 1 depth 140 random_delays|142     |142  |119.889          |7.453            |
|Tree n_branch 1 depth 160 random_delays|162     |162  |144.826          |9.371            |
|Tree n_branch 1 depth 180 random_delays|182     |182  |205.978          |11.889           |

N branches > 1

|Circuit name     |Vertices|Edges|Opt 1 time       |Opt 2 time       |
|-----------------|--------|-----|-----------------|-----------------|
|Tree n_branch 2 depth 1 random_delays|4       |5    |0.003            |0.003            |
|Tree n_branch 2 depth 2 random_delays|8       |11   |0.023            |0.030            |
|Tree n_branch 2 depth 3 random_delays|16      |23   |0.212            |0.120            |
|Tree n_branch 2 depth 4 random_delays|32      |47   |1.830            |0.497            |
|Tree n_branch 3 depth 1 random_delays|5       |7    |0.008            |0.007            |
|Tree n_branch 3 depth 2 random_delays|14      |22   |0.185            |0.094            |
|Tree n_branch 3 depth 3 random_delays|41      |67   |3.777            |0.690            |
|Tree n_branch 3 depth 4 random_delays|122     |202  |48.047           |4.397            |
|Tree n_branch 4 depth 1 random_delays|6       |9    |0.013            |0.012            |
|Tree n_branch 4 depth 2 random_delays|22      |37   |0.573            |0.233            |
|Tree n_branch 4 depth 3 random_delays|86      |149  |57.330           |3.548            |
|Tree n_branch 4 depth 4 random_delays|342     |597  |1673.138         |34.680           |


#### Graph data
|Circuit name     |Vertices|Edges|Opt 1 time       |Opt 2 time       |
|-----------------|--------|-----|-----------------|-----------------|
|Full graph 20 nodes random_delays|21      |192  |0.272            |0.434            |
|Full graph 40 nodes random_delays|41      |782  |3.145            |3.566            |
|Full graph 60 nodes random_delays|61      |1772 |4.635            |4.637            |
|Full graph 80 nodes random_delays|81      |3162 |19.618           |22.289           |
|Full graph 100 nodes random_delays|101     |4952 |36.925           |28.343           |
|Full graph 120 nodes random_delays|121     |7142 |43.694           |42.018           |
|Full graph 140 nodes random_delays|141     |9732 |79.382           |59.424           |
|Full graph 160 nodes random_delays|161     |12722|106.434          |92.594           |
|Full graph 180 nodes random_delays|181     |16112|135.168          |134.733          |



#### OPT 1 vs OPT 2
In this chart the two algorithm are compared. In particular, the aim is to show that OPT 2 outperforms OPT 1 when
we the circuits have a small amount of edges.
The followings bubble charts (generated with the script [plot.py](plot.py)) highlight this behavior. The size of the 
bubble represents the time used with OPT 1 and the color represents the time taken by OPT 2. 
So the bigger is the bubble and more time is been required for OPT 1 to complete, and more *'yellowish'* is the bubble
and more time is been needed for OPT 2.

As expected, OPT 2 scales very well with the number of vertices (the color of the biggest bubble is purple),
and increasing the number of edges (close to (V^2)/2 ), the performance starts to decrease rapidly.

The interactive plot can be found [here](doc/html/time_bench.html) (it requires to be opened with a browser/HTML reader).
<p align="center">
  <img width="80%" src="doc/images/time_bench.png"/>
</p>

## Memory benchmark
This section reports the memory consumed by the algorithms. I do not think the report is very detailed since Python is a
garbage collected language, and the measurement has been done through 
[memory profiler](https://pypi.org/project/memory-profiler/) that under the hood uses 
[psutil](https://pypi.org/project/psutil/).
The script responsible of the memory benchmark is [mem_parallel_benchamrk.py](mem_parallel_benchmark.py) and the memory
usage is been monitored with an interval of *10ns*.
The script monitors only the amount of memory needed to run the algorithm (so the memory needed for the graph has been
excluded).
The following table reports only the max delta memory consumption (in MB) of the large circuits:

|Circuit name     |Vertices|Edges| Δ Memory Opt 1     | Δ Memory Opt 2     |
|-----------------|--------|-----|-----------------|-----------------|
|Full graph 120 nodes|121     |7142 |0.25             |0.25             |
|Full graph 20 nodes random_delays|21      |192  |0.25             |0.25             |
|Full graph 40 nodes random_delays|41      |782  |0.25             |0.25             |
|Tree n_branch 1 depth 180 random_delays|182     |182  |1.22265625       |0.6328125        |
|Full graph 140 nodes random_delays|141     |9732 |1.84375          |1.7109375        |
|Full graph 140 nodes|141     |9732 |2.8515625        |1.890625         |
|Full graph 160 nodes random_delays|161     |12722|4.89453125       |2.78125          |
|Full graph 160 nodes|161     |12722|5.0625           |3.31640625       |
|Full graph 180 nodes random_delays|181     |16112|6.9453125        |4.49609375       |
|Full graph 180 nodes|181     |16112|7.96484375       |4.08203125       |
|Tree n_branch 4 depth 4 random_delays|342     |597  |35.4140625       |3.5              |
|Tree n_branch 4 depth 4|342     |597  |40.6171875       |1.6640625        |


# Author
* [Davide Yi Xian Hu](https://github.com/DragonBanana)