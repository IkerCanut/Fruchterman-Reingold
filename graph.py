#n, m, V, E
class Graph:
    def __init__(self, V, E):
        self.n = len(V)
        self.m = len(E)
        self.nodes = V
        self.edges = E
    
    def read(file_path):
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
            return Graph(V, E)
