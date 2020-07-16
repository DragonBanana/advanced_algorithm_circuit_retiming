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
The [gen_circuits.py](gen_circuits.py) contains the functions to generate different types of circuits:
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

## algorithm.py:
This script contains the implementation of 5 algorithms described by Charles E. Leiserson and James B. Saxe.
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

* **OPT_1**: Given a graph G and a matrix D. It returns a retimed graph with minimum legal clock.
```python
import algorithm, gen_circuits
G = gen_circuits.gen_correlator(4)
W, D = algorithm.WD(G)
retimed_G = algorithm.OPT_1(G, D)
```