import networkx as nx
import itertools

class Graph:
    ## The class provides the Graph object as wrapper for a networkx undirected Graph
    def __init__(self):
        self.G = nx.Graph()

    def __eq__(self,other):
        return nx.is_isomorphic(self.G, other.G)
               
    def add_vertex(self,v):
        self.G.add_node(v)

    def has_edge(self,u,v):
        return self.G.has_edge(u,v)
        
    def get_vertices(self):
        return list(self.G.nodes())
        
    def add_edge(self,u,v):
        self.G.add_edge(u,v)
        
    def get_edges(self):
        return list(self.G.edges())

    def add_vertices(self,v):
        self.G.add_nodes_from(v)
   

class Clause:
    ## The class provides the Clause object as a wrapper for a list of integers literals
    def __init__(self,literals):
        self.literals = literals
               
    def get_literals(self):
        return list(self.literals)

class Formula:
    ## This class provides the Formula object as a wrapper for a list of Clauses
    def __init__(self,clauses):
        self.clauses = [Clause(C) for C in clauses]

    def __repr__(self):
        return " & ".join(["({0})".format("|".join([str(L) for L in C.get_literals()])) for C in self.clauses])

    def all_clause(self,literals):
        self.clauses.append(Clause(literals))
        
    def get_clauses(self):
        return list(self.clauses)
        
    def __len__(self):
        return len(self.clauses)



def powerset(X):
    ## returns a list of all subsets of X (as tuples)
    return [S for k in xrange(len(X)+1) for S in subsets(X,k)]

def subsets(X,k):
    ## returns a list of all subsets of X of size k (as tuples)
    return list(itertools.combinations(X,k))


#########################################################
#########################################################

def clique_solver(G,k):

    for s in subsets(G.get_vertices(), k):
        counter = 0
        for pair in subsets(s, 2):
            if not G.has_edge(pair[0], pair[1]):
                break
            else:
                counter += 1
                if (counter == (k*(k-1))/2):
                    return True
    return False


def sat_to_clique(F):

    G = Graph()
    clauses = F.get_clauses()
    k = clauses.__len__()

    for i in range(k-1):
        for literal1 in clauses[i].get_literals(): # Pick a literal from current clause
            for j in range(i+1,k):
                for literal2 in clauses[j].get_literals(): # Take a literal from the other clause
                    if (literal1 != -literal2): # Connect if they are not opposite to each other
                        G.add_edge(float(str(literal1) + "." + str(i)), float(str(literal2) + "." + str(j)))
                    
    return (G,k)


def sat_solver(F):
    result = sat_to_clique(F)
    return clique_solver(result[0], result[1])

def is_satisfiable(B):
    if B: return "Formula is satisfiable\n" 
    else: return "Formula is not satisfiable\n"

def main():
    F1 = Formula([[3, -1], [-3, -5], [-3, -4], [1, -3], [4, 5], [1, 3]])
    print("Formula #1:", F1)
    print(is_satisfiable(sat_solver(F1)))

    F2 = Formula([[5, -1, -2, -4], [4, -1, -5], [1, 3, -4], [2, -1]])
    print("Formula #2:", F2)
    print(is_satisfiable(sat_solver(F2)))

    F3 = Formula([[-2, -4], [2, 3, 5, -4], [-1, -2, -3], [-1, -4]])
    print("Formula #3:", F3)
    print(is_satisfiable(sat_solver(F3)))

    F4 = Formula([[4, -5], [4, 5], [3, 4], [3, -4], [4, -2], [-3, -4]])
    print("Formula #4:", F4)
    print(is_satisfiable(sat_solver(F4)))

main()
