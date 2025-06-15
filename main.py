from graph import Graph
def main():
    g = Graph(5, representation="adjacency_list")
    g.read_graph("input.txt")

    # informacoes gerais
    g.write_graph_info("info.txt")

    # busca em largura (BFS)
    pais_bfs, niveis_bfs = g.bfs(start=1)
    g.write_search_tree(pais_bfs, niveis_bfs, "bfs.txt")

    # busca em profundidade (DFS)
    pais_dfs = g.dfs(start=1)
    g.write_search_tree(pais_dfs, {v: -1 for v in pais_dfs}, "dfs.txt") 

    # componentes conexos
    g.write_components("componentes.txt")


if __name__ == "__main__":
    main()
