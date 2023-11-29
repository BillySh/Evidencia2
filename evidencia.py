#Carlos Damian Suarez Bernal, Humberto Ivan Ulloa Cardona, Pablo Ceballos Gutierrez


#-----------------------------------------Import-----------------------------------------------------------------
import math
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np
import ast
from collections import defaultdict

maxS = float('inf') #Starting comparison tents to infinity.

#-----------------------------------------Functions--------------------------------------------------------------

#Copy of temp solution

def copyToFinal(path):
    final_path[:N + 1] = path[:] #Slice finalpath from beggining to N from a copy of path
    final_path[N] = path[0] #Change positon N on finalpath to be the value of path at index 0

#Find first minimum edge cost -> This takes and returns the minimum weight corresponding to index i
def firstMin(adj, i):
    min = maxS #Equal to infinite
    for d in range(N):
        if adj[i][d] < min and i != d: #Weight at [i][d] is less thand current min and differnt to d
            min = adj[i][d]
    return min

#Find second minimum edge cost -> end at vertex i
def secondMin(adj, i):
    first, second =  maxS, maxS #Initialize first and second at current maxS
    for d in range(N):
        if i == d: #If index in i is equal to d in range N, continue avoid looping
            continue
        if adj[i][d] <= first: #Changes values so that first is equal to adj[i][d] and sets second to be the previous first
            second = first
            first =  adj[i][d]
        elif(adj[i][d] <= second and adj[i][d] != first):
            second = adj[i][d]
    return second #After runnning all of the vertex, return the second weight

def TSPRec(adj, curr_bound, curr_weight, level, curr_path, visited): #Explore to find the solution an save it, this uses Depth first with backtracking
    global final_res #Global variable

    if level == N: #Base case, covered all nodes
        if adj[curr_path[level - 1]][curr_path[0]] != 0:
            curr_res = curr_weight + adj[curr_path[level - 1]][curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res #Save the solution
        return 
    
    for i in range(N):  #This allows to search nodes in range N 
        if(adj[curr_path[level-1]][i] != 0 and visited[i] == False):
            temp = curr_bound 
            curr_weight += adj[curr_path[level - 1]][i]

            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level-1]) + firstMin(adj,i))/2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level-1]) + firstMin(adj,i))/2)
            
            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True
                TSPRec (adj, curr_bound, curr_weight, level + 1, curr_path, visited) #Next level, recurssion
            
            #Reset all changes done to curr_weight and bound
            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp

            visited = [False] * len(visited)
            for d in range(level):
                if curr_path[d] != -1:
                    visited[curr_path[d]] =  True

#Setting the final path to follow.

def TSP(adj,N):
    curr_bound = 0 
    curr_path = [-1] * (N+1)
    visited = [False] * N 
    for i in range(N):
        curr_bound += (firstMin(adj, i)+secondMin(adj,i))
    #Round to integer
    curr_bound = math.ceil(curr_bound/2)

    visited[0] = True
    curr_path[0] = 0
    #Call TSPRec for current weight
    TSPRec(adj, curr_bound, 0,1, curr_path, visited)


class GrafoFlujoMax:
    def __init__(self, graph):
        self.graph = graph
        self.ROW = len(graph)


    # Using BFS as a searching algorithm 
    def searching_algo_BFS(self, s, t, parent):

        visited = [False] * (self.ROW)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    # Applying fordfulkerson algorithm
    def ford_fulkerson(self, source, sink):
        parent = [-1] * (self.ROW)
        max_flow = 0

        while self.searching_algo_BFS(source, sink, parent):

            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Adding the path flows
            max_flow += path_flow

            # Updating the residual values of edges
            v = sink
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow




#------------------------------------Main-------------------------------------

def main():

    #Open file and read a matrix
    
    with open('input2.txt', 'r') as f:
        l = [[int(num) for num in line.split(',')] for line in f]
    
    #Var declaration
    global N 
    N = l[0][0]
    l.remove(l[0])
    adj = l


    global final_path
    final_path = [None] * (N + 1)
    global visited
    visited= [False] * N #Fill of Falses
    global final_res
    final_res = maxS
    TSP(adj,N)

    #Open the file with the flux between nodes

    with open('input3.txt', 'r') as f:
        l2 = [[int(num) for num in line.split(',')] for line in f]    

    global M 
    M = l2[0][0]
    adj2 = l2



    #---------------Results------------------
    print("--------------------------Parte 1--------------------------")
    

    with open('input4.txt', 'r') as f:
        a = np.array([ast.literal_eval(line) for line in f])
    print("\n--------------------------Parte 2--------------------------")
    #print("Cantidad minima de cableado:", final_res)
    print(final_path)
    print("Camino para recorrer las colonias:", end = ' ')
    for i in range(N+1):
        print(final_path[i], end= ' ')
    print("\n--------------------------Parte 3--------------------------")
    grafoFlujoMAximo = GrafoFlujoMax(adj2)
    d = 0
    o = N-1
    print(f"Flujo máximo recorrdio: {grafoFlujoMAximo.ford_fulkerson(d, o) }")
    
    print("--------------------------Parte 4--------------------------")
    points = np.array (a)
    vor = Voronoi(points)

    fig = voronoi_plot_2d(vor)
    plt.show()

if __name__ == "__main__":
    main()