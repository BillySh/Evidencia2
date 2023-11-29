#!/usr/bin/env python3

import heapq

def prim(graph):
    num_vertices = len(graph)
    visited = [False] * num_vertices
    min_heap = [(0, 0)]

    while min_heap:
        weight, current_vertex = heapq.heappop(min_heap)

        if not visited[current_vertex]:
            visited[current_vertex] = True
            print(f"Conectar colonia 0 a colonia {current_vertex} con una distancia de {weight} km")

            for neighbor, neighbor_weight in graph[current_vertex]:
                heapq.heappush(min_heap, (neighbor_weight, neighbor))

def read_input(file_path):
    graph = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            row = list(map(int, line.strip().split()))
            graph.append(row)
    return graph

def build_graph(matrix):
    graph = [[] for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                graph[i].append((j, matrix[i][j]))
                graph[j].append((i, matrix[i][j]))
    return graph
