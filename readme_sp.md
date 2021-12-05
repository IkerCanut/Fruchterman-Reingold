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

# Parámetros
* **-v**, **--verbose**: Bandera que activa los comentarios durante la ejecución.
* **-i**, **--iterations**: Número máximo de iteraciones permitido. Default: 400.
* **-t**, **--temperature**: Temperatura inicial del programa. Default: 100.
* **-d**, **--damping**: Factor de amortiguamiento de la temperatura. Default: 0.977.
* **-c**, **--constant**: Constante para modificar el esparcimiento. Default: 1.3.
* **-w**, **--width**: Ancho del frame. Default: 1000.
* **-m**, **--margin**: Multiplicador para ajustar el tamaño del grafo. Default: 1.8.
* **-na**, **--not-animated**: Bandera para no animar el algoritmo.
* **-p**, **--pause**: Tiempo entre frame y frame. Default: 0.01.
* **-r**, **--refresh**: Cantidad de iteraciones entre frame y frame. Default: 10.
* Además, se debe especificar el archivo en donde se encuentra el gráfico.