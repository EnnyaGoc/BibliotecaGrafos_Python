import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt


class BellmanFordStepApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bellman-Ford Passo a Passo")
        self.graph = nx.DiGraph()
        self.dist = {}
        self.iteration = 0
        self.max_iterations = 0
        self.edge_list = []
        self.source = None

        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Adicionar Vértice", command=self.add_vertex).pack()
        tk.Button(self.root, text="Adicionar Aresta", command=self.add_edge).pack()
        tk.Button(self.root, text="Iniciar Bellman-Ford", command=self.init_bellman_ford).pack()
        tk.Button(self.root, text="Próxima Iteração", command=self.next_iteration).pack()
        tk.Button(self.root, text="Mostrar Grafo", command=self.draw_graph).pack()

        self.output = tk.Text(self.root, height=20, width=50)
        self.output.pack()

    def add_vertex(self):
        node = simpledialog.askstring("Novo Vértice", "Nome do vértice:")
        if node:
            self.graph.add_node(node)

    def add_edge(self):
        u = simpledialog.askstring("Aresta", "Vértice de origem:")
        v = simpledialog.askstring("Aresta", "Vértice de destino:")
        w = simpledialog.askfloat("Peso", "Peso da aresta:")
        if u and v and w is not None:
            self.graph.add_edge(u, v, weight=w)

    def init_bellman_ford(self):
        self.source = simpledialog.askstring("Origem", "Vértice de origem:")
        if self.source not in self.graph:
            messagebox.showerror("Erro", "Vértice de origem não existe!")
            return

        self.dist = {v: float('inf') for v in self.graph.nodes}
        self.dist[self.source] = 0
        self.edge_list = list(self.graph.edges(data=True))
        self.iteration = 0
        self.max_iterations = len(self.graph.nodes) - 1

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Inicialização:\n{self.format_distances()}\n")

    def next_iteration(self):
        if self.iteration >= self.max_iterations:
            messagebox.showinfo("Fim", "Todas as iterações foram executadas.")
            return

        updated = False
        for u, v, d in self.edge_list:
            if self.dist[u] + d['weight'] < self.dist[v]:
                self.dist[v] = self.dist[u] + d['weight']
                updated = True

        self.iteration += 1
        self.output.insert(tk.END, f"\nIteração {self.iteration}:\n{self.format_distances()}\n")

        if not updated:
            self.output.insert(tk.END, "Nenhuma atualização — algoritmo pode ser encerrado.\n")
            self.iteration = self.max_iterations  # força encerramento

    def draw_graph(self):
        pos = nx.spring_layout(self.graph)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        plt.figure(figsize=(8, 6))
        nx.draw(self.graph, pos, with_labels=True, node_size=800, node_color='lightgreen')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.title("Grafo Atual")
        plt.show()

    def format_distances(self):
        result = ""
        for v in sorted(self.dist):
            val = self.dist[v]
            if val == float('inf'):
                result += f"{v}: ∞  "
            else:
                result += f"{v}: {val}  "
        return result


if __name__ == "__main__":
    root = tk.Tk()
    app = BellmanFordStepApp(root)
    root.mainloop()
