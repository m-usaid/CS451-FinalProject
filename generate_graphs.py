import networkx as nx 
import matplotlib.pyplot as plt 

def read_data(filename: str) -> list:
    listOfEdges = []
    with open (filename, 'r') as file:
        for l in file:
            tokens = l.split()
            if tokens[0] == 'e':
                edge = (tokens[1], tokens[2])
                listOfEdges.append(edge)
    return listOfEdges

def create_graph(filename: str) -> nx.Graph:
    # construct networkx graph from file 
    graph = nx.Graph()
    edgeList = read_data(filename)
    graph.add_edges_from(edgeList)
    return graph   

def draw_graph(G: nx.Graph):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.savefig('Data/graph_out/graph-{0}.png'.format(len(G)))
    # plt.savefig('graph.png')
    # plt.show()

files = [
    'Data/myciel3.col',
    'Data/myciel4.col',
    'Data/gcol1.txt',
    'Data/gcol23.txt'
    ]

def generate_graphs(files):
    graphs = []
    for file in files:
        graphs.append(create_graph(file))
    for graph in graphs:
        draw_graph(graph)


generate_graphs(files)
