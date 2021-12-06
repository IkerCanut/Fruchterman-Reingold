#n, m, V, E
class Graph:
    def __init__(self, V, E):
        '''
        Initializes Graph object
        Parameters:
        V:  node list
        E:  edge list
        '''
        self.n = len(V)
        self.m = len(E)
        self.nodes = V
        self.edges = E
    
    def read(file_path):
        '''Reads the graph from a file.
           Required file format:
           n
           [V]
           [E]
           
           where:
           n    is the nomber of nodes
           [V]  is the node list
           [E]  is the edge list'''
        with open(file_path, 'r') as f:
            lines = f.readlines()
            n = int(lines[0].strip())
            V = []
            for i in range(1, n+1):
                V.append(lines[i].strip())
            E = []
            for i in range(n+1, len(lines)):
                e = lines[i].strip().split(' ')
                E.append((e[0], e[1]))
            return Graph(V, E)
