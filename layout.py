import matplotlib.pyplot as plt
import numpy as np
from numpy import random


class Layout:

    def __init__(self, graph, verbose, iters, temp, damp, width, margin, animate, c, pause, refresh):
        '''
        Initializes Layout object
        Parameters:
        graph:      Graph object to plot
        verbose:    activate comments during execution
        iters:      max number of iterations permitted
        temp:       initial temperature
        damp:       temperature's damping factor
        c:          algorithm's force constant
        width:      frame width
        margin:     multiplier to adjust graph size
        animate:    animate the plot
        pause:      time between frames, if animated
        refresh:    frames between plots, if animated
        '''

        self.graph = graph
        self.verbose = verbose
        self.iters = iters
        self.temp = temp
        self.damp = damp
        self.c = c
        self.width = width
        self.margin = margin
        self.animate = animate
        self.pause = pause
        self.refresh = refresh

        # Dictionary representing nodes positions
        self.pos = {}
        # Dictionary representing accumulated forces for each node
        self.accum = {}
        # Frame area
        self.area = self.width * self.width
        # Algorithm's constant
        self.k = self.c * np.sqrt(self.area/self.graph.n)

    def fa(self, dist):
        '''Calculates attraction force between 2 neighboring nodes'''
        return dist*dist / self.k

    def fr(self, dist):
        '''Calculates repulsion force between 2 neighboring nodes'''
        return self.k*self.k / dist

    def randomize_positions(self):
        '''Randomizes initial positions'''
        print("Randomizing positions\n") if self.verbose else None
        for v in self.graph.nodes:
            self.pos[v] = [random.uniform(-0.5*self.width, 0.5*self.width),
                           random.uniform(-0.5*self.width, 0.5*self.width)]

    def initialize_accumulators(self):
        '''Sets accum values to 0'''
        for v in self.graph.nodes:
            self.accum[v] = [0, 0]

    def clamp_eps(self, dist):
        '''Sets 0 distance to eps, avoiding 0 division'''
        eps = 0.05
        dist = eps if dist < eps else dist
        return dist

    def compute_attraction_forces(self):
        '''Computes the attraction force between each pair of
           neighboring nodes'''
        for u, v in self.graph.edges:
            distance = np.sqrt((self.pos[u][0] - self.pos[v][0]) ** 2 +
                               (self.pos[u][1] - self.pos[v][1]) ** 2)

            fx = distance * (self.pos[v][0] - self.pos[u][0]) / self.k
            fy = distance * (self.pos[v][1] - self.pos[u][1]) / self.k
            self.accum[u][0] += fx
            self.accum[u][1] += fy
            self.accum[v][0] -= fx
            self.accum[v][1] -= fy

    def compute_repulsion_forces(self):
        '''Computes the attraction force between each pair of nodes'''
        for u in self.graph.nodes:
            for v in self.graph.nodes:
                if v != u:
                    distance = np.sqrt((self.pos[u][0] - self.pos[v][0]) ** 2 +
                                       (self.pos[u][1] - self.pos[v][1]) ** 2)

                    fx = self.k*self.k / distance * \
                        (self.pos[v][0] - self.pos[u][0]) / distance
                    fy = self.k*self.k / distance * \
                        (self.pos[v][1] - self.pos[u][1]) / distance
                    # We go through each pair twice, so we halve forces
                    self.accum[u][0] -= fx/2
                    self.accum[u][1] -= fy/2
                    self.accum[v][0] += fx/2
                    self.accum[v][1] += fy/2

    def compute_gravity_forces(self):
        '''Computes the attraction gravity force for each node'''
        for v in self.graph.nodes:
            distance = np.sqrt(self.pos[v][0] ** 2 +
                               self.pos[v][1] ** 2)

            fx = distance * (self.pos[v][0]) / self.k
            fy = distance * (self.pos[v][1]) / self.k
            # 1 order of magnitude less
            self.accum[v][0] -= fx / 10
            self.accum[v][1] -= fy / 10

    def update_positions(self, i):
        '''Updates positions with the previously calculated values'''
        if (self.verbose):
            print("\nIteration N° %d: Forces: " % i)
            for v in self.graph.nodes:
                print("Node %s: \t X axis = %f \t Y axis = %f" %
                      (v, self.accum[v][0], self.accum[v][1]))

        for v in self.graph.nodes:
            modulo = np.sqrt(self.accum[v][0] ** 2 + self.accum[v][1] ** 2)
            if modulo > self.temp:
                self.accum[v][0] *= self.temp / modulo
                self.accum[v][1] *= self.temp / modulo

            self.pos[v][0] += self.accum[v][0]
            self.pos[v][1] += self.accum[v][1]

            # To avoid getting outside the window
            cte = self.margin-0.1
            if self.pos[v][0] < -cte*self.width:
                self.pos[v][0] = -cte*self.width
            if self.pos[v][1] < -cte*self.width:
                self.pos[v][1] = -cte*self.width
            if self.pos[v][0] > cte*self.width:
                self.pos[v][0] = cte*self.width
            if self.pos[v][1] > cte*self.width:
                self.pos[v][1] = cte*self.width

    def update_temperature(self):
        '''Updates temperature with the damping factor'''
        self.temp *= self.damp

    def draw(self):
        '''Draws nodes (and edges) in its current positions'''
        # Clear the frame
        plt.clf()
        # Don't plot the axes
        plt.axis('off')
        # Fix the window's size
        plt.xlim(-self.margin*self.width,  self.margin*self.width)
        plt.ylim(-self.margin*self.width,  self.margin*self.width)

        for (a, b) in self.graph.edges:
            x = [self.pos[a][0], self.pos[b][0]]
            y = [self.pos[a][1], self.pos[b][1]]
            plt.plot(x, y, marker='.', markersize=10)
        # Pause between frames
        plt.pause(self.pause)

    def layout(self):
        '''Applies Fruchtermann-Reingold algorithm to layout the graph'''

        print("Graph has %d nodes" % self.graph.n) if self.verbose else None
        print("and %d edges" % self.graph.m) if self.verbose else None

        plt.figure("Graph plot")
        self.randomize_positions()

        if(self.verbose):
            print("Initial positions:")
            for v in self.graph.nodes:
                print("Node %03s \t X position = %f \t Y Position = %f" %
                      (v, self.pos[v][0], self.pos[v][1]))
            print()

        min_t = 0.05
        print("Waiting until graph cools completely or iterations run short") if self.verbose else None
        print("You can add several options to the program, run next time with -h or --help to see") if self.verbose else None
        for i in range(self.iters):
            self.initialize_accumulators()
            self.compute_attraction_forces()
            self.compute_repulsion_forces()
            self.compute_gravity_forces()
            self.update_positions(i)
            self.update_temperature()
            if i % self.refresh == 0 and self.animate:
                self.draw()
            if self.temp < min_t:
                print("Graph cooled completely") if self.verbose else None
                print("Number of iterations: %d" % i) if self.verbose else None
                break

        self.draw()
        print(
            "\nAlgorithm finished! Beautiful graph, by the way ;)") if self.verbose else None
        print("When you're done admiring it, you can close the window") if self.verbose else None
        plt.show()
