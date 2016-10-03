import networkx as nx
import strings_to_synsets
import matplotlib.pyplot as plt

def process(strings):
    final = []
    synsetslist = strings_to_synsets.get_all_synsets(strings)
    print(synsetslist)
    G = nx.Graph() #creo il grafo

    for synset in synsetslist:
        G.add_node(synset, name=synset) #aggiungo tanti nodi quanti sono i synsets

    for i in range(0, (len(G.nodes()) - 1)):
        for j in range(i + 1, (len(G.nodes()) - 1)):
            score = G.nodes()[i].path_similarity(G.nodes()[j])
            G.add_edge(G.nodes()[i], G.nodes()[j], weight=score)

    print(G.edges())


    print(G.number_of_nodes())
    print(G.number_of_edges())

    pos = nx.spring_layout(G)
    nx.draw(G, pos)
    node_labels = nx.get_node_attributes(G, 'name')
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, labels=edge_labels)
    plt.show()

    return final

