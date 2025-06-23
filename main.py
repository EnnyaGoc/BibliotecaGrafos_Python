from graph import Graph
def main():
    g = Graph(5, representation="adjacency_list")
    g.read_graph("input.txt")

    # informacoes gerais
    g.write_graph_info("info.txt")
    print("Arquivo info.txt gerado com informações do grafo.")


    # busca em largura (BFS)
    pais_bfs, niveis_bfs = g.bfs(start=1)
    g.write_search_tree(pais_bfs, niveis_bfs, "bfs.txt")

    # busca em profundidade (DFS)
    pais_dfs = g.dfs(start=1)
    g.write_search_tree(pais_dfs, {v: -1 for v in pais_dfs}, "dfs.txt") 

    # componentes conexos
    g.write_components("componentes.txt")


 #Caminho mínimo usando Dijkstra
    origem = 1
    destino = 8

    caminho, distancia = g.shortest_path(origem, destino)
    print(f"Caminho mínimo de {origem} até {destino}: {caminho} com distância {distancia}")

    #Distância de um vértice para todos
    distancias, _ = g.dijkstra(origem)
    print(f"Distâncias do vértice {origem} para todos os outros vértices:")
    for v, d in distancias.items():
        print(f"{origem} -> {v}: {d}")


if __name__ == "__main__":
    main()