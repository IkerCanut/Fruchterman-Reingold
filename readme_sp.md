[English](readme.md)

# Resumen
Presentamos una implementación del algoritmo Fruchterman-Reingold para visualización de grafos, realizada en Python3. Este es un algoritmo que plantea un sistema de fuerzas, el cual trata a las aristas como resortes, que acercan a los nodos que estan conectados, en un intento de encontrar un equilibrio que minimice la energía del sistema. Además, existen fuerzas repulsivas entre cada par de nodos, al igual que la repulsión de dos imanes de la misma polaridad. Nosotros buscamos obtener imágenes estéticamente agradables y este programa permite, con sus numerosos parámetros, cambiar el resultado.

# Dependencias
Para poder ejecutar el programa, se deben instalar los siguientes paquetes:
```bash
    python3 -m pip install -U pip
    python3 -m pip install -U matplotlib
    python3 -m pip install -U numpy
```

# Ejemplo
Nosotros presentamos este código con algunos grafos, de esta manera se puede probar:
```bash
    python3 main.py -i 400 --verbose grafos/malla.txt
```

# Formato de grafos
En la primer linea tenemos la cantidad de vértices. En las siguientes n lineas, tenemos el nombre de cada nodo. Finalmente, tenemos las aristas, con los vértices en los cuales inciden separados por un espacio.
* [Cantidad de Vértices]
* [Nombre del Vértice 0]
* ...
* [Nombre del Vértice n]
* [Nombre del Vértice u] [Nombre del Vértice v]
* ...

Un ejemplo de un simple triangulo podría ser:
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