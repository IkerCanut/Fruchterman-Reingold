#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Ejemplo parseo argumentos

import argparse
import matplotlib.pyplot as plt
import numpy as np


class LayoutGraph:

    def __init__(self, grafo, iters, refresh, c1, c2, verbose=False):
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

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        V, E = self.grafo
        posiciones = {}

        for v in V:
            posiciones[v] = (np.random.randn(), np.random.randn())

        for (a, b) in E:
            x = [posiciones[a][0], posiciones[b][0]]
            y = [posiciones[a][1], posiciones[b][1]]
            plt.plot(x, y, marker='.', markersize=10)

        plt.show()

        accum = {}
        for v in V:
            accum[v] = [0, 0]

        # Atraccion
        for i in range(self.iters):
            for (a, b) in E:
                fx = posiciones[b][0] - posiciones[a][0]
                fy = posiciones[b][1] - posiciones[a][1]
                accum[a][0] += fx
                accum[a][1] += fy
                accum[b][0] -= fx
                accum[b][1] -= fy

        # Repulsion
        for a in V:
            for b in V:
                if (a != b):
                    fx = posiciones[a][0] - posiciones[b][0]
                    fy = posiciones[a][1] - posiciones[b][1]
                    accum[a][0] += fx
                    accum[a][1] += fy
                    accum[b][0] -= fx
                    accum[b][1] -= fy

        # TODO: VER BIEN LOS SIGNOS!!
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
        help='Muestra mas informacion al correr el programa'
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

    args = parser.parse_args()

    # Descomentar abajo para ver funcionamiento de argparse
    print(args.verbose)
    print(args.iters)
    print(args.file_name)
    print(args.temp)
    # return

    grafo = lee_grafo_archivo(args.file_name)

    # # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo,
        iters=args.iters,
        refresh=1,
        c1=0.1,
        c2=5.0,
        verbose=args.verbose
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
