#Carlos Damian Suarez Bernal, Humberto Ivan Ulloa Cardona, Pablo Ceballos Gutierrez


#-----------------------------------------Import-----------------------------------------------------------------
import math
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

def main():

    #Open file and read a matrix
    
    with open('input_part1.txt', 'r') as f:
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

    #---------------Results------------------
    print("--------------------------Parte 1--------------------------")
    print("Cantidad minima de cableado:", final_res)
    print("Camino para cablear las colonias:", end = ' ')
    for i in range(N+1):
        print(final_path[i], end= ' ')
    print("\n--------------------------Parte 2--------------------------")
    print("--------------------------Parte 3--------------------------")
    print("--------------------------Parte 4--------------------------")

if __name__ == "__main__":
    main()