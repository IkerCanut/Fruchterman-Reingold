#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Ejemplo parseo argumentos

import argparse
import matplotlib.pyplot as plt
import numpy as np
from numpy import random


class LayoutGraph:

    def __init__(self, grafo, iters, refresh, c1, c2, verbose, width, height):
        """
        Parámetros:
        grafo: grafo en formato lista
        iters: cantidad de iteraciones a realizar
        refresh: cada cuántas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        c1: constante de repulsión
        c2: constante de atracción
        verbose: si está encendido, activa los comentarios
        """

        # Guardo el grafo
        self.grafo = grafo

        # Inicializo estado
        # Completar
        self.posiciones = {}
        self.fuerzas = {}

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2
        self.width = width
        self.height = height

    def calcular_k(self, area, n, c):
        return c * np.sqrt(area/n)

    def fa(self, d, k):
        return (d ** 2.0) / k

    def fr(self, d, k):
        return (k ** 2.0) / d

    def randomize_positions(self, V, posiciones):
        for v in V:
            posiciones[v] = [random.uniform(
                0, self.width), random.uniform(0, self.height)]

    def initialize_accumulators(self, V, accum):
        for v in V:
            accum[v] = [0, 0]

    def compute_attraction_forces(self, V, E, pos, accum):
        c = 1.8
        k = self.calcular_k(self.width * self.height, len(V), c)
        for u, v in E:
            distance = np.sqrt((pos[u][0] - pos[v][0]) ** 2 +
                               (pos[u][1] - pos[v][1]) ** 2)
            if distance == 0:
                distance = 0.05
            mod_fa = self.fa(distance, k)
            fx = mod_fa * (pos[v][0] - pos[u][0]) / distance
            fy = mod_fa * (pos[v][1] - pos[u][1]) / distance
            accum[u][0] += fx
            accum[u][1] += fy
            accum[v][0] -= fx
            accum[v][1] -= fy

    def compute_repulsion_forces(self, V, pos, accum):
        c = 1.8
        k = self.calcular_k(self.width * self.height, len(V), c)
        for u in V:
            for v in V:
                if u != v:
                    distance = np.sqrt((pos[u][0] - pos[v][0]) ** 2 +
                                       (pos[u][1] - pos[v][1]) ** 2)
                    if (distance == 0):
                        distance = 0.05
                    mod_fr = self.fr(distance, k)
                    fx = mod_fr * (pos[v][0] - pos[u][0]) / distance
                    fy = mod_fr * (pos[v][1] - pos[u][1]) / distance
                    accum[u][0] -= fx
                    accum[u][1] -= fy
                    accum[v][0] += fx
                    accum[v][1] += fy

    def update_positions(self, V, pos, accum):
        print(accum)
        for v in V:
            pos[v][0] += accum[v][0]
            pos[v][1] += accum[v][1]
            if pos[v][0] < 0:
                pos[v][0] = 0
            if pos[v][1] < 0:
                pos[v][1] = 0
            if pos[v][0] > self.width:
                pos[v][0] = self.width
            if pos[v][1] > self.height:
                pos[v][1] = self.height

    def draw(self, E, posiciones):
        plt.clf()

        for (a, b) in E:
            x = [posiciones[a][0], posiciones[b][0]]
            y = [posiciones[a][1], posiciones[b][1]]
            plt.plot(x, y, marker='.', markersize=10)

        plt.pause(1)

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        V, E = self.grafo

        posiciones = {}
        accum = {}

        self.randomize_positions(V, posiciones)
        self.draw(E, posiciones)

        for i in range(self.iters):
            self.initialize_accumulators(V, accum)
            self.compute_attraction_forces(V, E, posiciones, accum)
            self.compute_repulsion_forces(V, posiciones, accum)
            self.update_positions(V, posiciones, accum)
            self.draw(E, posiciones)

        # for v in V:
        #    print(v + " " + str(posiciones[v][0]) + " " + str(posiciones[v][1]))
        # print(accum)


def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Verbosidad, opcional, False por defecto
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa',
        default=False
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=50
    )
    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=100.0
    )
    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )
    # Ancho maximo
    parser.add_argument(
        '--width',
        type=float,
        help='Ancho maximo',
        default=1500.0
    )
    # Altura maxima
    parser.add_argument(
        '--height',
        type=float,
        help='Altura maxima',
        default=1000.0
    )

    args = parser.parse_args()

    # Descomentar abajo para ver funcionamiento de argparse
    print(args.verbose)
    print(args.iters)
    print(args.file_name)
    print(args.temp)
    print(args.width)
    print(args.height)
    # return

    grafo = lee_grafo_archivo(args.file_name)

    # # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo,
        iters=args.iters,
        refresh=1,
        c1=0.1,
        c2=5.0,
        verbose=args.verbose,
        width=args.width,
        height=args.height
    )

    # # Ejecutamos el layout
    layout_gr.layout()
    return


def lee_grafo_archivo(file_path):
    '''
    Lee un grafo desde un archivo y devuelve su representacion como lista.
    Ejemplo Entrada: 
        3
        A
        B
        C
        A B
        B C
        C B
    Ejemplo retorno: 
        (['A','B','C'],[('A','B'),('B','C'),('C','B')])
    '''
    with open(file_path, 'r') as f:
        lines = f.readlines()
        v = int(lines[0].strip())
        V = []
        for i in range(1, v+1):
            V.append(lines[i].strip())
        E = []
        for i in range(v+1, len(lines)):
            e = lines[i].strip().split(' ')
            E.append((e[0], e[1]))
        return (V, E)


if __name__ == '__main__':
    main()
