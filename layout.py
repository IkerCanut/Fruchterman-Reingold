import matplotlib.pyplot as plt
import numpy as np
from numpy import random


class Layout:
    
    def __init__(self, graph, iters, refresh, verbose, width, height, temp, c, p, d):
        """
        Params:
        graph: graph en formato lista
        iters: cantidad de iteraciones a realizar
        refresh: cada cuántas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        verbose: si está encendido, activa los comentarios
        """

        self.graph = graph
        self.positions = {}
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
        self.area = self.width * self.height
        self.k = self.c * np.sqrt(self.area/self.graph.n)
    
    
    def fa(self, d):
        return d*d / self.k

    def fr(self, d):
        return self.k*self.k / d

    def randomize_positions(self, positions):
        for v in self.graph.nodes:
            positions[v] = [random.uniform(0, 0.5*self.width),
                            random.uniform(0, 0.5*self.height)]

    def initialize_accumulators(self, accum):
        for v in self.graph.nodes:
            accum[v] = [0, 0]

    def compute_attraction_forces(self, pos, accum):
        for u, v in self.graph.edges:
            distance = np.sqrt((pos[u][0] - pos[v][0]) ** 2 +
                               (pos[u][1] - pos[v][1]) ** 2)
            if distance == 0:
                distance = 0.05
            mod_fa = self.fa(distance)
            fx = mod_fa * (pos[v][0] - pos[u][0]) / distance
            fy = mod_fa * (pos[v][1] - pos[u][1]) / distance
            accum[u][0] += fx
            accum[u][1] += fy
            accum[v][0] -= fx
            accum[v][1] -= fy

    def compute_repulsion_forces(self, pos, accum):
        for u in self.graph.nodes:
            for v in self.graph.nodes:
                if v != u:
                    distance = np.sqrt((pos[u][0] - pos[v][0]) ** 2 +
                                       (pos[u][1] - pos[v][1]) ** 2)
                    if (distance == 0):
                        distance = 0.05
                    mod_fr = self.fr(distance)
                    fx = mod_fr * (pos[v][0] - pos[u][0]) / distance
                    fy = mod_fr * (pos[v][1] - pos[u][1]) / distance
                    accum[u][0] -= fx/2     #Estamos calculando 2 veces para cada par
                    accum[u][1] -= fy/2
                    accum[v][0] += fx/2
                    accum[v][1] += fy/2

    def compute_gravity_forces(self, pos, accum):
        centro_x = self.width/2
        centro_y = self.height/2

        for v in self.graph.nodes:
            distance = np.sqrt((centro_x - pos[v][0]) ** 2 +
                               (centro_y - pos[v][1]) ** 2)
            if distance == 0:
                distance = 0.05
            mod_fa = self.fa(distance)
            fx = mod_fa * (pos[v][0] - centro_x) / distance
            fy = mod_fa * (pos[v][1] - centro_y) / distance
            accum[v][0] -= fx / 10
            accum[v][1] -= fy / 10

    def update_positions(self, pos, accum):
        for v in self.graph.nodes:
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

    def draw(self, positions):
        plt.clf()
        LEFT_BOUND, RIGHT_BOUND = -2000, 2000
        BOTTOM_BOUND, TOP_BOUND = -2000, 2000
        plt.xlim(LEFT_BOUND, RIGHT_BOUND)
        plt.ylim(BOTTOM_BOUND, TOP_BOUND)
        
        for (a, b) in self.graph.edges:
            x = [positions[a][0], positions[b][0]]
            y = [positions[a][1], positions[b][1]]
            plt.plot(x, y, marker='.', markersize=10)

        plt.pause(self.p)

    def layout(self):
        """
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        """

        positions = {}
        accum = {}

        self.randomize_positions(positions)
        self.draw(positions)

        for i in range(self.iters):
            self.initialize_accumulators(accum)
            self.compute_attraction_forces(positions, accum)
            self.compute_repulsion_forces(positions, accum)
            self.compute_gravity_forces(positions, accum)
            self.update_positions(positions, accum)
            self.update_temperature()
            self.draw(positions)
