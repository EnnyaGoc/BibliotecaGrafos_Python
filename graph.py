from collections import deque

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        #Para cada número i (que representa um vértice), você cria uma chave i no dicionário e associa a essa chave uma lista vazia []
        self.adjacency_list = {i: [] for i in range(1, num_vertices + 1)}
        #Cria uma lista com num_vertices elementos, todos igual a 0.
        #Esse for vai repetir o processo de criação da lista [0, 0, 0] para cada vértice. Ou seja, vai criar tantas listas quantos forem os vértices do grafo.
        #O _ é uma convenção para indicar que o valor da variável não é importante.
        self.adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]
        
    def read_graph(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        self.num_vertices = int(lines[0].strip())
        
        for line in lines[1:]:
            u, v = map(int, line.strip().split())
            self.add_edge(u, v)

    def add_edge(self, u, v):
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)

        self.adjacency_matrix[u-1][v-1] = 1
        self.adjacency_matrix[v-1][u-1] = 1

    def write_graph_info(self, file_path):
        grau_medio, distribuicao = self.calculate_degree_info()
        with open(file_path, 'w') as f:
            f.write(f"Vertices: {self.num_vertices}\n")
            f.write(f"Arestas: {self.calculate_edges()}\n")
            f.write(f"Grau Medio: {grau_medio}\n")
            f.write(f"Distribuicao do Grau: {distribuicao}\n")

    def calculate_edges(self):
        """Calcula o número total de arestas"""
        return sum(len(neighbors) for neighbors in self.adjacency_list.values()) // 2
    
    def calculate_degree_info(self):
        """Calcula o grau médio e a distribuição do grau dos vértices"""
        degrees = {v: len(neighbors) for v, neighbors in self.adjacency_list.items()}
        grau_medio = sum(degrees.values())/ self.num_vertices
        distribuicao = {}

        for grau in degrees.values():
            distribuicao[grau] = distribuicao.get(grau, 0) + 1
        
        return grau_medio, distribuicao
    
    def bfs(self, start):
        """Realiza a busca em largura (BFS)"""
        visited = {v: False for v in self.adjacency_list}
        level = {v: -1 for v in self.adjacency_list}
        parent = {v: None for v in self.adjacency_list}

        queue = deque([start])
        visited[start] = True
        level[start] = 0

        while queue:
            u = queue.popleft()
            for v in self.adjacency_list[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    level[v] = level[u] + 1
                    queue.append(v)

        return parent, level

    def dfs(self, start):
        """Realiza a busca em profundidade (DFS)"""
        visited = {v: False for v in self.adjacency_list}
        parent = {v: None for v in self.adjacency_list}
        self._dfs_recursive(start, visited, parent)

        return parent
    
    def _dfs_recursive(self, u, visited, parent):
        visited[u] = True
        for v in self.adjacency_list[u]:
            if not visited[v]:
                parent[v] = u
                self._dfs_recursive(v, visited, parent)

    def connected_components(self):
        """Encontra os componentes conexos do grafo"""
        visited = {v: False for v in self.adjacency_list}
        components = []

        for v in self.adjacency_list:
            if not visited[v]:
                component = []
                self._dfs_for_components(v, visited, component)
                components.append(component)

        return components
    
    def _dfs_for_components(self, u, visited, component):
        visited[u] = True
        component.append(u)
        for v in self.adjacency_list[u]:
            if not visited[v]:
                self._dfs_for_components(v, visited, component)
