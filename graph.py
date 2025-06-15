from collections import deque

class Graph:
    def __init__(self, num_vertices, representation="adjacency_list"):
        self.num_vertices = num_vertices
        self.representation = representation
        
        if representation == "adjacency_list":
            self.adjacency_list = {i: [] for i in range(1, num_vertices + 1)}
        elif representation == "adjacency_matrix":
            self.adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]
        
    def read_graph(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        self.num_vertices = int(lines[0].strip())

        if self.representation == "adjacency_list":
            self.adjacency_list = {i: [] for i in range(1, self.num_vertices + 1)}
        elif self.representation == "adjacency_matrix":
            self.adjacency_matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]

        for line in lines[1:]:
            u, v = map(int, line.strip().split())
            self.add_edge(u, v)

    def add_edge(self, u, v):
        if self.representation == "adjacency_list":
            self.adjacency_list[u].append(v)
            self.adjacency_list[v].append(u)
        elif self.representation == "adjacency_matrix":
            self.adjacency_matrix[u-1][v-1] = 1
            self.adjacency_matrix[v-1][u-1] = 1

    def write_graph_info(self, file_path):
        grau_medio, distribuicao = self.calculate_degree_info()
        with open(file_path, 'w') as f:
            f.write(f"Vertices: {self.num_vertices}\n")
            f.write(f"Arestas: {self.calculate_edges()}\n")
            f.write(f"Grau Medio: {grau_medio:.2f}\n")
            f.write(f"Distribuicao do Grau:\n")
            for grau in sorted(distribuicao):
                f.write(f"{grau}: {distribuicao[grau]}\n")

    def calculate_edges(self):
        if self.representation == "adjacency_list":
            return sum(len(v) for v in self.adjacency_list.values()) // 2
        elif self.representation == "adjacency_matrix":
            total = 0
            for i in range(self.num_vertices):
                for j in range(i + 1, self.num_vertices):
                    if self.adjacency_matrix[i][j] == 1:
                        total += 1
            return total

    def calculate_degree_info(self):
        degrees = {}

        if self.representation == "adjacency_list":
            degrees = {v: len(neigh) for v, neigh in self.adjacency_list.items()}

        elif self.representation == "adjacency_matrix":
            for i in range(self.num_vertices):
                grau = sum(self.adjacency_matrix[i])
                degrees[i + 1] = grau

        grau_medio = sum(degrees.values()) / self.num_vertices

        distribuicao = {}
        for grau in degrees.values():
            distribuicao[grau] = distribuicao.get(grau, 0) + 1

        return grau_medio, distribuicao


    def bfs(self, start):
        visited = {v: False for v in range(1, self.num_vertices + 1)}
        level = {v: -1 for v in range(1, self.num_vertices + 1)}
        parent = {v: None for v in range(1, self.num_vertices + 1)}

        queue = deque([start])
        visited[start] = True
        level[start] = 0

        while queue:
            u = queue.popleft()
            neighbors = self.adjacency_list[u] if self.representation == "adjacency_list" else [
                v + 1 for v in range(self.num_vertices) if self.adjacency_matrix[u-1][v] == 1
            ]

            for v in neighbors:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    level[v] = level[u] + 1
                    queue.append(v)

        return parent, level

    def dfs(self, start):
        visited = {v: False for v in range(1, self.num_vertices + 1)}
        parent = {v: None for v in range(1, self.num_vertices + 1)}
        self._dfs_recursive(start, visited, parent)
        return parent

    def _dfs_recursive(self, u, visited, parent):
        visited[u] = True
        neighbors = self.adjacency_list[u] if self.representation == "adjacency_list" else [
            v + 1 for v in range(self.num_vertices) if self.adjacency_matrix[u-1][v] == 1
        ]
        for v in neighbors:
            if not visited[v]:
                parent[v] = u
                self._dfs_recursive(v, visited, parent)

    def write_search_tree(self, parent, level, file_path):
        with open(file_path, 'w') as f:
            f.write("Pai de cada vertice:\n")
            for v in sorted(parent):
                f.write(f"{v}: {parent[v]}\n")
            f.write("\nNivel de cada vertice:\n")
            for v in sorted(level):
                f.write(f"{v}: {level[v]}\n")

    def connected_components(self):
        visited = {v: False for v in range(1, self.num_vertices + 1)}
        components = []

        for v in visited:
            if not visited[v]:
                comp = []
                self._dfs_component(v, visited, comp)
                components.append(comp)

        return components

    def _dfs_component(self, u, visited, comp):
        visited[u] = True
        comp.append(u)

        neighbors = self.adjacency_list[u] if self.representation == "adjacency_list" else [
            v + 1 for v in range(self.num_vertices) if self.adjacency_matrix[u-1][v] == 1
        ]
        for v in neighbors:
            if not visited[v]:
                self._dfs_component(v, visited, comp)

    def write_components(self, file_path):
            components = self.connected_components()
            components.sort(key=len, reverse=True)

            with open(file_path, 'w') as f:
                f.write(f"Numero de componentes conexas: {len(components)}\n\n")
                for i, comp in enumerate(components, 1):
                    f.write(f"Componente {i} (tamanho {len(comp)}): {sorted(comp)}\n")
