from fib import get_fib as fancy_function
import matplotlib.pyplot as plt
import networkx as nx
import inspect
import ast
import os


def dfs(node, graph: nx.DiGraph):
    graph.add_node(type(node))
    for child in ast.iter_child_nodes(node):
        graph.add_edge(type(node), dfs(child, graph))
    return type(node)


def create_graph():
    ast_obj = ast.parse(inspect.getsource(fancy_function))
    graph = nx.DiGraph()
    dfs(ast_obj, graph)
    return graph


def draw(g: nx.DiGraph):
    plt.figure(figsize=(20, 20), dpi=80)
    subax1 = plt.subplot()
    options = {
        "node_size": 1500,
        "alpha": 0.9,
    }
    nx.draw(g, with_labels=True, **options)
    if not os.path.exists('artifacts/'):
        os.makedirs('artifacts')
    plt.savefig('artifacts/result.png')
    plt.show()


def main():
    graph = create_graph()
    draw(graph)


if __name__ == '__main__':
    main()