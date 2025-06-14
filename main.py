from graph import Graph
def main():
    g = Graph(5)
    g.read_graph("input.txt")

    g.write_graph_info("output.txt")

    parent,level = g.bfs(1)
    print("BFS - Pais:", parent)
    print("BFS - Niveis:", level)

    parent = g.dfs(1)
    print("DFS - Pais:", parent)

    components = g.connected_components()
    print("Componentes conexos: ", components)


if __name__ == "__main__":
    main()
