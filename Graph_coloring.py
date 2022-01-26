import argparse
from pyvis.network import Network

def create_nodes(size: int):
    nodes = []
    for i in range(size):
        nodes.append(chr(97+i))

    return nodes

def nodes_label(graph, labels):
    nodes_attributes = graph.get_nodes()
    if len(labels) == len(nodes_attributes):
        for i in range(len(labels)):
            graph.get_node(nodes_attributes[i])['label'] = labels[i]

def create_edges(adj_matrix):
    edges = []
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            if adj_matrix[i][j] == 1:
                edges.append([chr(97+i), chr(97+j)])
    return edges

def get_degree_of_each_node(adj_matrix):
    nodes_degree = {}
    for i in range(len(adj_matrix)):
        nodes_degree[i] = adj_matrix[i].count(1)

    return nodes_degree

def sort_by_degree(nodes_degree):
    return dict(sorted(nodes_degree.items(), key=lambda x:x[1], reverse=True)) 

def color_node(net, node, color):
    net.get_node(node)['color'] = color

def visualization_graph_colored(graph, labels=[]):
    nodes = create_nodes(len(graph))
    edges = create_edges(graph)
    net = Network('1920x', '1080px')
    net.add_nodes(nodes)
    net.add_edges(edges)
    coloring_graph(net, graph)

    if labels:
        nodes_label(net, labels)

    file_save = 'Graph.html'
    net.show(file_save)

def get_node_is_not_adjacency_of(node, adj_matrix):
    adjacencies = adj_matrix[node]
    list_nodes = []
    for i in range(len(adjacencies)):
        if adjacencies[i] == 0:
            list_nodes.append(i)

    return list_nodes

def is_exist_adj_colored_node(colored, node, adj_matrix):
    if colored:
        for colored_node in colored:
            if adj_matrix[colored_node][node] == 1:
                return True
    return False

def coloring_graph(graph, adj_matrix):
    nodes_list_sorted = sort_by_degree(get_degree_of_each_node(adj_matrix=adj_matrix))
    color = ['red', 'blue', 'green', 'black', 'purple', 'orange', 'yellow']
    color_th = 0
    list_colored_nodes = []

    for node in nodes_list_sorted:
        colored = []
        if node not in list_colored_nodes:
            list_nodes = get_node_is_not_adjacency_of(node, adj_matrix)
            graph.get_node(chr(97+node))['color'] = color[color_th]
            list_colored_nodes.append(node)
            colored.append(node)

            for not_adj_node in list_nodes:
                if not_adj_node not in list_colored_nodes and not is_exist_adj_colored_node(colored, not_adj_node, adj_matrix):
                    graph.get_node(chr(97+not_adj_node))['color'] = color[color_th]
                    list_colored_nodes.append(not_adj_node)
                    colored.append(not_adj_node)

            color_th+=1

def build_graph(path_name: str):
    try:
        adjacency_matrix = []
        with open(path_name) as f:
            row = []
            data = f.read()
            rows = data.split('\n')
            for row in rows:
                adjacency_matrix.append([int(num) for num in row.split(" ")])
        return adjacency_matrix
    except:
        print('Cannot build graph')

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path_name', dest='path', help='Path name for building graph', required=True)
    parser.add_argument('-l', '--labels', dest='labels', help='(Optional) Labels for all vertices in graph')
    args = parser.parse_args()

    labels = []
    if args.labels:
        labels = [label for label in args.labels.split(',')]
    graph = build_graph(args.path)
    visualization_graph_colored(graph, labels)