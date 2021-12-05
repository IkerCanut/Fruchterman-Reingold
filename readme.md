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
