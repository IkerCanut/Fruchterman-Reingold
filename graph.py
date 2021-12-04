#n, m, V, E
class Graph:
    def __init__(self, V, E):
        self.n = len(V)
        self.m = len(E)
        self.nodes = V
        self.edges = E
        
