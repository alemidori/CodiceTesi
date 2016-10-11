import networkx as nx
import strings_to_synsets
import matplotlib.pyplot as plt
import numpy as np

def process(strings, param_similarity, num_synset):
    flatten = lambda l: sum(map(flatten, l), []) if isinstance(l, list) else [l]
    print("\n\n*************INIZIO METODO GRAPH_RELATIONS")
    synset_to_strings = []
    synsetslist = strings_to_synsets.get_all_synsets(strings, num_synset)
    print("I synset sono: "+str(len(synsetslist)))
    print(synsetslist)
    G = nx.Graph() #creo il grafo

    for synset in synsetslist:
        G.add_node(synset, name=synset.lemmas()[0].name()) #aggiungo tanti nodi quanti sono i synsets

    for i in range(0, (len(G.nodes()) - 1)):
        for j in range(i + 1, (len(G.nodes()) - 1)):
            score = G.nodes()[i].path_similarity(G.nodes()[j])
            if score > param_similarity: #se sono sufficientemente simili nel grafo di wordnet allora crea un
                # arco tra i due nodi
                G.add_edge(G.nodes()[i], G.nodes()[j], weight=score)

    degree_centrality_dict = nx.degree_centrality(G)
    print("Degree centrality dict: " +str(degree_centrality_dict))

    if sum(degree_centrality_dict.values()) != 0.0:
        percentile = np.percentile(list(degree_centrality_dict.values()), 90)

        for synset_centr in degree_centrality_dict.keys():
            if degree_centrality_dict[synset_centr] > percentile: #se sono abbastanza centrali
                print(str(synset_centr)+str(degree_centrality_dict[synset_centr]))
                synset_to_strings.append(synset_centr.lemmas()[0].name())
        if not synset_to_strings:
            print("Termini con centralità inferiore al percentile:")
            synset_to_strings.append([el.lemmas()[0].name() for el in degree_centrality_dict.keys()])

    else:
        print("Termini con centralità = 0.0:")
        synset_to_strings.append([el.lemmas()[0].name() for el in degree_centrality_dict.keys()])

    final = list(set(flatten(synset_to_strings)))
    print("Nuova lista di termini dai synset: " + str(final))
    #print(G.number_of_nodes())
    #print(G.number_of_edges())

    pos = nx.spring_layout(G, scale=2)
    nx.draw(G, pos)
    node_labels = nx.get_node_attributes(G, 'name')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, labels=edge_labels)
    plt.savefig('graph.png')

    print('\n' + str(final))
    return final

