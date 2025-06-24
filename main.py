from graph import Graph

def main():
    g = Graph(5, representation="adjacency_list")
    g.read_graph("input.txt")

    g.write_graph_info("info.txt")
    print("Arquivo info.txt gerado com informações do grafo.")

    pais_bfs, niveis_bfs = g.bfs(start=1)
    g.write_search_tree(pais_bfs, niveis_bfs, "bfs.txt")
    print("Arquivo bfs.txt gerado com os resultados da BFS.")

    pais_dfs = g.dfs(start=1)
    g.write_search_tree(pais_dfs, {v: -1 for v in pais_dfs}, "dfs.txt")
    print("Arquivo dfs.txt gerado com os resultados da DFS.")

    g.write_components("componentes.txt")
    print("Arquivo componentes.txt gerado com os componentes conexos.")

    origem = 1
    destino = 8
    caminho, distancia = g.shortest_path(origem, destino)
    distancias, _ = g.dijkstra(origem)

    with open("dijkstra.txt", "w") as f:
        f.write(f"Caminho mínimo de {origem} até {destino}: {caminho} com distância {distancia}\n\n")
        f.write(f"Distâncias do vértice {origem} para todos os outros vértices:\n")
        for v, d in distancias.items():
            f.write(f"{origem} -> {v}: {d}\n")
    print("Arquivo dijkstra.txt gerado com os resultados do Dijkstra.")

if __name__ == "__main__":
    main()
