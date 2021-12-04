import matplotlib.pyplot as plt
import numpy as np
from numpy import random


class Layout:
    
    def __init__(self, grafo, iters, refresh, verbose, width, height, temp, c, p, d):
        """
        Parámetros:
        grafo: grafo en formato lista
        iters: cantidad de iteraciones a realizar
        refresh: cada cuántas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        verbose: si está encendido, activa los comentarios
        """

        self.grafo = grafo
        self.posiciones = {}
        self.fuerzas = {}
        self.iters = iters
        self.verbose = verbose
        self.refresh = refresh
        self.width = width
        self.height = height
        self.temp = temp
        self.c = c
        self.p = p
        self.ct = d

    def calc_k(self, area, n, c):
        return c * np.sqrt(area/n)

    def fa(self, d, k):
        return d*d / k

    def fr(self, d, k):
        return k*k / d

    def randomize_positions(self, V, posiciones):
        for v in V:
            posiciones[v] = [random.uniform(
                0, 0.5*self.width), random.uniform(0, 0.5*self.height)]

    def initialize_accumulators(self, V, accum):
        for v in V:
            accum[v] = [0, 0]

    def compute_attraction_forces(self, V, E, pos, accum, c):
        k = self.calc_k(self.width * self.height, len(V), c)
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

    def compute_repulsion_forces(self, V, pos, accum, c):
        k = self.calc_k(self.width * self.height, len(V), c)
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

    def compute_gravity_forces(self, V, pos, accum, c):
        k = self.calc_k(self.width * self.height, len(V), c)

        centro_x = self.width/2
        centro_y = self.height/2

        for v in V:
            distance = np.sqrt((centro_x - pos[v][0]) ** 2 +
                               (centro_y - pos[v][1]) ** 2)
            if distance == 0:
                distance = 0.05
            mod_fa = self.fa(distance, k)
            fx = mod_fa * (pos[v][0] - centro_x) / distance
            fy = mod_fa * (pos[v][1] - centro_y) / distance
            accum[v][0] -= fx / 10
            accum[v][1] -= fy / 10

    def update_positions(self, V, pos, accum):
        for v in V:
            modulo = np.sqrt(accum[v][0] ** 2 + accum[v][1] ** 2)
            if modulo > self.temp:
                accum[v][0] *= self.temp / modulo
                accum[v][1] *= self.temp / modulo

            pos[v][0] += accum[v][0]
            pos[v][1] += accum[v][1]

            '''if pos[v][0] < 0:
                pos[v][0] = 0
            if pos[v][1] < 0:
                pos[v][1] = 0
            if pos[v][0] > self.width:
                pos[v][0] = self.width
            if pos[v][1] > self.height:
                pos[v][1] = self.height'''

    def update_temperature(self):
        ct = self.ct
        self.temp *= ct
        #print(self.temp)

    def draw(self, E, posiciones):
        plt.clf()

        for (a, b) in E:
            x = [posiciones[a][0], posiciones[b][0]]
            y = [posiciones[a][1], posiciones[b][1]]
            plt.plot(x, y, marker='.', markersize=10)

        plt.pause(self.p)

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """
        (V, E) = (self.grafo.nodes, self.grafo.edges)

        posiciones = {}
        accum = {}

        c = self.c

        self.randomize_positions(V, posiciones)
        self.draw(E, posiciones)

        for i in range(self.iters):
            self.initialize_accumulators(V, accum)
            self.compute_attraction_forces(V, E, posiciones, accum, c)
            self.compute_repulsion_forces(V, posiciones, accum, c)
            self.compute_gravity_forces(V, posiciones, accum, c)
            self.update_positions(V, posiciones, accum)
            self.update_temperature()
            self.draw(E, posiciones)
