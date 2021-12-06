[Castellano](readme_sp.md)

# Summary
We present an implementation of the Fruchterman-Reingold algorithm for graph visualization, made in Python3. This is a force-directed layout algorithm that treats edges like springs, which move nodes closer in an attempt to find an equilibrium that minimizes the energy of the system. Moreover, there are repulsive forces between every pair of nodes, just like the repulsion of two magnets of the same polarity. We strive for aesthetically-pleasing pictures of graphs, and this program allows, with its numerous parameters, to change the outcome.

# Dependencies
In order to run this program, you need to install the following packages:
```bash
    python3 -m pip install -U pip
    python3 -m pip install -U matplotlib
    python3 -m pip install -U numpy
```

# Example
We present this code with a few graphs, so you can try it out:
```bash
    python3 main.py -i 400 --verbose grafos/malla.txt
```

# Graph Formatting
In the first line we have the number of nodes. Then, the following n lines represent the name of each vertex. Finally, we have the edges, with its incident nodes separated with a space.
* [Number of Nodes]
* [Name of Node 0]
* ...
* [Name of Node n]
* [Name of Node u] [Name of Node v]
* ...

An example of a simple triangle could be:
* 3
* a
* b
* c
* a b
* b c
* c a

# Parameters
* **-v**, **--verbose**: Activate comments during executions.
* **-i**, **--iterations**: Maximum number of iterations permitted. Default: 400.
* **-t**, **--temperature**: Initial temperature. Default: 100.
* **-d**, **--damping**: Temperature's damping factor. Default: 0.977.
* **-c**, **--constant**: Algorithm's force constant to modify the spread. Default: 1.3.
* **-w**, **--width**: Frame width. Default: 1000.
* **-m**, **--margin**: Multiplier to adjust graph size. Default: 1.8.
* **-na**, **--not-animated**: Flag to not animate the plot.
* **-p**, **--pause**: Time between frames. Default: 0.01
* **-r**, **--refresh**: Frames between plots. Default: 10.
* In addition, you need to specify the file in which the graph is located.

# References
1. THOMAS M. J. FRUCHTERMAN, EDWARD M. REINGOLD. Graph Drawing by Force–Directed Placement, Department of Computer Science, University of Illinois at Urbana-Champaign, 1304 W. Springfield Avenue, Urbana, IL 61801-2987, U.S.A.
