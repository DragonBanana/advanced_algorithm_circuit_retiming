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
This repository contains the implementation of two algorithm: **OPT_1** and **OPT_2**. Both the algorithms are described
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

## Circuit generator:
The [gen_circuits.py](gen_circuits.py) contains the functions to generate different types of circuits:
* N bit correlator.
* Tree with B branches and D depth.
* Close to fully connected graph with N nodes.
For most of the circuits is possible to choose randomize the delay of each node.
<p align="center">
  <img width="50%" src="doc/images/correlator_4_bit.png"/>
</p>
<p align="center">
  <img width="50%" src="doc/images/bin_tree_2_level.png"/>
</p>
