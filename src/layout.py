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
            distance = self.clamp_eps(distance)

            fx = distance * (self.pos[v][0] - self.pos[u][0]) / self.k
            fy = distance * (self.pos[v][1] - self.pos[u][1]) / self.k
            self.accum[u][0] += fx
            self.accum[u][1] += fy
            self.accum[v][0] -= fx
            self.accum[v][1] -= fy

    def compute_repulsion_forces(self):
        '''Computes the repulsion force between each pair of nodes'''
        for u in self.graph.nodes:
            for v in self.graph.nodes:
                if v != u:
                    distance = np.sqrt((self.pos[u][0] - self.pos[v][0]) ** 2 +
                                       (self.pos[u][1] - self.pos[v][1]) ** 2)
                    distance = self.clamp_eps(distance)

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
            distance = self.clamp_eps(distance)

            fx = distance * (self.pos[v][0]) / self.k
            fy = distance * (self.pos[v][1]) / self.k
            # 1 order of magnitude less
            self.accum[v][0] -= fx / 10
            self.accum[v][1] -= fy / 10

    def update_positions(self, i):
        '''Updates positions with the previously calculated values'''
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

    def draw(self, color):
        '''Draws nodes (and edges) in its current positions'''
        # Clear the frame
        plt.clf()
        # Don't plot the axes
        plt.axis('off')
        # Fix window size
        plt.xlim(-self.margin*self.width,  self.margin*self.width)
        plt.ylim(-self.margin*self.width,  self.margin*self.width)

        # Change the background color depending on temperature
        figure = plt.figure("Graph plot")
        figure.set_facecolor((color, (1-color)/1.5, 1-color, 0.2+color/4.0))

        for (u, v) in self.graph.edges:
            x = [self.pos[u][0], self.pos[v][0]]
            y = [self.pos[u][1], self.pos[v][1]]
            plt.plot(x, y, marker='.', markersize=10)
        # Pause between frames
        plt.pause(self.pause)

    def layout(self):
        '''Applies Fruchtermann-Reingold algorithm to layout the graph'''

        print("Hi!\nGraph has %d nodes and %d edges" %
              (self.graph.n, self.graph.m)) if self.verbose else None

        plt.figure("Graph plot")
        self.randomize_positions()

        if self.verbose:
            print("Initial positions:")
            for v in self.graph.nodes:
                print("Node %03s \t X position = %f \t Y Position = %f" %
                      (v, self.pos[v][0], self.pos[v][1]))
            print()

        temp0 = self.temp
        min_t = 0.05
        print("Waiting until graph cools completely or iterations run short") if self.verbose else None
        print("You can add several options to the program, run next time with -h or --help to see\n") if self.verbose else None

        for i in range(self.iters):
            self.initialize_accumulators()
            self.compute_attraction_forces()
            self.compute_repulsion_forces()
            self.compute_gravity_forces()
            self.update_positions(i)
            self.update_temperature()

            if i % self.refresh == 0 and self.animate:
                color = self.temp/temp0
                self.draw(color if color < 1 else 1)
            if self.temp < min_t:
                print("Graph cooled completely") if self.verbose else None
                print("Number of iterations: %d" % i) if self.verbose else None
                break

        if self.temp >= min_t:
            print("Iterations ran short") if self.verbose else None
            print("Number of iterations: %d" %
                  self.iters) if self.verbose else None

        print() if self.verbose else None

        if self.verbose:
            print("Final positions:")
            for v in self.graph.nodes:
                print("Node %03s \t X position = %f \t Y Position = %f" %
                      (v, self.pos[v][0], self.pos[v][1]))
            print()

        color = self.temp/temp0
        self.draw(color if color < 1 else 1)
        print(
            "Algorithm finished! Beautiful graph, by the way ;)") if self.verbose else None
        print("When you're done admiring it, you may close the window") if self.verbose else None
        plt.show()
