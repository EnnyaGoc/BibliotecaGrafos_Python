import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BellmanFordStepApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bellman-Ford Passo a Passo")

        self.graph = nx.DiGraph()
        self.dist = {}
        self.pred = {}
        self.iteration = 0
        self.edge_idx = 0
        self.total_bf_iterations = 0
        self.edge_list = []
        self.source = None
        self.has_negative_cycle = False
        self.algorithm_finished = False

        self.highlighted_edge = None
        self.updated_node = None
        self.has_updated_in_iteration = False

        self.create_widgets()
        self.create_graph_canvas()

    def create_widgets(self):
        graph_controls = tk.LabelFrame(self.root, text="Controle do Grafo", padx=5, pady=5)
        graph_controls.pack(padx=10, pady=5, fill="x")
        tk.Button(graph_controls, text="Adicionar Vértice", command=self.add_vertex).pack(side=tk.LEFT, padx=5)
        tk.Button(graph_controls, text="Adicionar Aresta", command=self.add_edge).pack(side=tk.LEFT, padx=5)
        tk.Button(graph_controls, text="Resetar Grafo", command=self.reset_graph).pack(side=tk.LEFT, padx=5)

        bf_controls = tk.LabelFrame(self.root, text="Controle Bellman-Ford", padx=5, pady=5)
        bf_controls.pack(padx=10, pady=5, fill="x")
        self.init_button = tk.Button(bf_controls, text="Iniciar Bellman-Ford", command=self.init_bellman_ford)
        self.init_button.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(bf_controls, text="Próxima Ação", command=self.next_action)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.next_button.config(state=tk.DISABLED)

        self.output = tk.Text(self.root, height=15, width=80, wrap=tk.WORD)
        self.output.pack(padx=10, pady=5)

    def create_graph_canvas(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6), facecolor='#f0f0f0')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(padx=10, pady=5, expand=True, fill="both")
        self.pos = None
        plt.ion()
        self.draw_graph()

    def reset_graph(self):
        self.graph = nx.DiGraph()
        self.dist = {}
        self.pred = {}
        self.iteration = 0
        self.edge_idx = 0
        self.total_bf_iterations = 0
        self.edge_list = []
        self.source = None
        self.has_negative_cycle = False
        self.algorithm_finished = False
        self.highlighted_edge = None
        self.updated_node = None
        self.pos = None

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "Grafo resetado.\n")
        self.init_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)
        self.draw_graph()
        messagebox.showinfo("Reset", "Grafo e algoritmo resetados.")

    def add_vertex(self):
        node = simpledialog.askstring("Novo Vértice", "Nome do vértice:")
        if node:
            if node in self.graph.nodes:
                messagebox.showwarning("Aviso", f"'{node}' já existe.")
            else:
                self.graph.add_node(node)
                self.output.insert(tk.END, f"Vértice '{node}' adicionado.\n")
                self.pos = None
                self.draw_graph()

    def add_edge(self):
        u = simpledialog.askstring("Aresta", "Origem:")
        v = simpledialog.askstring("Aresta", "Destino:")
        if not all(n in self.graph.nodes for n in [u, v]):
            messagebox.showerror("Erro", "Origem ou destino inexistente.")
            return
        try:
            w = simpledialog.askfloat("Peso", f"Peso da aresta {u} → {v}:")
            if w is None:
                return
        except:
            messagebox.showerror("Erro", "Peso inválido.")
            return
        self.graph.add_edge(u, v, weight=w)
        self.output.insert(tk.END, f"Aresta {u} --{w}--> {v} adicionada.\n")
        self.draw_graph()

    def init_bellman_ford(self):
        if not self.graph.nodes:
            messagebox.showerror("Erro", "Adicione vértices e arestas.")
            return
        self.source = simpledialog.askstring("Origem", "Vértice de origem:")
        if self.source not in self.graph:
            messagebox.showerror("Erro", "Origem inválida.")
            return

        self.dist = {v: float('inf') for v in self.graph.nodes}
        self.pred = {v: None for v in self.graph.nodes}
        self.dist[self.source] = 0
        self.edge_list = list(self.graph.edges(data=True))
        self.iteration = 0
        self.edge_idx = 0
        self.total_bf_iterations = len(self.graph.nodes)
        self.has_updated_in_iteration = False
        self.algorithm_finished = False
        self.highlighted_edge = None
        self.updated_node = None

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Começando de '{self.source}'\nIteração 1:\n")
        self.output.insert(tk.END, self.format_distances())
        self.draw_graph()
        self.init_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_action(self):
        if self.algorithm_finished:
            messagebox.showinfo("Fim", "Algoritmo concluído.")
            self.next_button.config(state=tk.DISABLED)
            return
        if self.source is None:
            messagebox.showwarning("Aviso", "Inicie o algoritmo primeiro.")
            return
        if self.edge_idx == 0:
            self.has_updated_in_iteration = False

        if self.edge_idx < len(self.edge_list):
            u, v, data = self.edge_list[self.edge_idx]
            weight = data['weight']
            self.highlighted_edge = (u, v)
            self.updated_node = None

            self.output.insert(tk.END, f"\n{u} --{weight}--> {v}: ")

            if self.dist[u] != float('inf') and self.dist[u] + weight < self.dist[v]:
                self.dist[v] = self.dist[u] + weight
                self.pred[v] = u
                self.updated_node = v
                self.has_updated_in_iteration = True
                self.output.insert(tk.END, f"dist[{v}] atualizado para {self.dist[v]:.2f}")
            else:
                self.output.insert(tk.END, "sem mudança")

            self.edge_idx += 1
            self.draw_graph()

        if self.edge_idx == len(self.edge_list):
            self.output.insert(tk.END, f"\n\nIteração {self.iteration + 1} concluída.\n")
            self.output.insert(tk.END, self.format_distances())
            self.iteration += 1
            self.edge_idx = 0
            self.highlighted_edge = None
            self.updated_node = None

            if not self.has_updated_in_iteration and self.iteration < self.total_bf_iterations - 1:
                self.output.insert(tk.END, "\nSem mudanças nesta rodada. Encerrando o algoritmo.\n")
                self.algorithm_finished = True
                self.next_button.config(state=tk.DISABLED)
                return

            if self.iteration == self.total_bf_iterations:
                self.output.insert(tk.END, "\nChecando ciclos negativos...\n")
                for u, v, data in self.edge_list:
                    if self.dist[u] != float('inf') and self.dist[u] + data['weight'] < self.dist[v]:
                        self.output.insert(tk.END, "Ciclo negativo detectado.\n")
                        self.has_negative_cycle = True
                        break
                if not self.has_negative_cycle:
                    self.output.insert(tk.END, "Nenhum ciclo negativo encontrado.\n")
                self.algorithm_finished = True
                self.next_button.config(state=tk.DISABLED)
            else:
                self.output.insert(tk.END, f"Iteração {self.iteration + 1}:\n")
                self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        self.ax.set_facecolor('#f9f9f9')

        if not self.graph.nodes:
            self.ax.text(0.5, 0.5, "Grafo Vazio", ha='center', va='center', transform=self.ax.transAxes, fontsize=16, color='gray')
            self.ax.set_title("Grafo Atual")
            self.canvas.draw_idle()
            return

        current_edges = list(self.graph.edges(data=True))
        if self.pos is None or len(self.graph.nodes) != len(self.pos):
            self.pos = nx.spring_layout(self.graph, seed=42)

        node_colors = []
        for node in self.graph.nodes:
            if node == self.source:
                node_colors.append('#FFD700')
            elif node == self.updated_node:
                node_colors.append('#FF6347')
            else:
                node_colors.append('#87CEEB')

        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, node_size=1200, node_color=node_colors,
                               edgecolors='#333', linewidths=1.5)

        edge_colors = ['black'] * len(current_edges)
        edge_widths = [1.5] * len(current_edges)
        if self.highlighted_edge:
            for i, (u, v, _) in enumerate(current_edges):
                if (u, v) == self.highlighted_edge:
                    edge_colors[i] = '#0000CD'
                    edge_widths[i] = 3.0
                    break

        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax,
                               edgelist=[(u, v) for u, v, _ in current_edges],
                               width=edge_widths, edge_color=edge_colors,
                               arrowsize=20, connectionstyle='arc3,rad=0.1')

        labels = {n: f"{n}\n(∞)" if self.dist.get(n, float('inf')) == float('inf') else f"{n}\n({self.dist[n]:.2f})"
                  for n in self.graph.nodes}
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax, labels=labels,
                                font_size=10, font_weight='bold', font_color='#333')

        weights = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, ax=self.ax, edge_labels=weights,
                                     font_color='darkgreen', font_size=9,
                                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

        self.ax.set_title("Grafo Atual", size=13, color='#444')
        self.ax.axis('off')
        plt.tight_layout()
        self.canvas.draw_idle()

    def format_distances(self):
        return ''.join(f"{v}: ∞\t" if self.dist[v] == float('inf') else f"{v}: {self.dist[v]:.2f}\t"
                       for v in sorted(self.dist)) + "\n"

if __name__ == "__main__":
    root = tk.Tk()
    app = BellmanFordStepApp(root)
    root.mainloop()
