from __future__ import division
import networkx as nx
import strings_to_synsets
import matplotlib.pyplot as plt
import numpy as np


def process(tuples):
    print("\n\n*************INIZIO METODO GRAPH_RELATIONS")
    flatten = lambda l: sum(map(flatten, l), []) if isinstance(l, list) else [l]
    tuples = flatten(tuples)
    print(tuples)
    synset_to_strings = []
    synsetslist = strings_to_synsets.get_all_synsets([k[0] for k in tuples])
    #print("I synset sono: "+str(len(synsetslist)))
    print(synsetslist)
    G = nx.Graph() #creo il grafo
    final = []
    for synset in synsetslist:
        G.add_node(synset, name=synset.lemmas()[0].name()) #aggiungo tanti nodi quanti sono i synsets
        print(synset)
    if len(synsetslist) > 1:
        for i in range(0, (len(G.nodes()) - 1)):
            for j in range(i + 1, (len(G.nodes()) - 1)):
                score = G.nodes()[i].path_similarity(G.nodes()[j])
                if score > 0.3: #se sono sufficientemente simili nel grafo di wordnet allora crea un
                    # arco tra i due nodi
                    G.add_edge(G.nodes()[i], G.nodes()[j], weight=score)

        if len(G) > 1:
            degree_centrality_dict = nx.degree_centrality(G)
            #print("Degree centrality dict: " +str(degree_centrality_dict))

            if sum(degree_centrality_dict.values()) != 0.0:
                percentile = np.percentile(list(degree_centrality_dict.values()), 90)
                #print("Percentile: "+str(percentile))
                for synset_centr in degree_centrality_dict.keys():
                    if degree_centrality_dict[synset_centr] >= percentile: #se sono abbastanza centrali
                        #print(str(synset_centr)+str(degree_centrality_dict[synset_centr]))
                        synset_to_strings.append((synset_centr.lemmas()[0].name(), degree_centrality_dict[synset_centr]))
                # if synset_to_strings:
                #     print("Termini con centralità maggiore o uguale al percentile.")

            else:
                #print("Termini con centralità = 0.0.")
                synset_to_strings.append([(el.lemmas()[0].name(), degree_centrality_dict[el])
                                          for el in degree_centrality_dict.keys()])
        else:
            print(len(G))
            # se il grafo ha solo un nodo la centralita' non puo' essere calcolata
            synset_to_strings.append(([n.lemmas()[0].name() for n in G.nodes()], 0))

        final = synset_to_strings
        print(final)
        final = flatten(final)
        final = list(set(final))
    elif len(synsetslist) == 0:
        for t in tuples:
            print(t[0])
            final.append([t[0]])
    else:
        for synset in synsetslist:
            print(synset)
            final.append(synset.lemmas()[0].name())

    #print("Nuova lista di termini dai synset: " + str(final))
    #print(G.number_of_nodes())
    #print(G.number_of_edges())

    pos = nx.spring_layout(G, scale=2)
    nx.draw(G, pos)
    node_labels = nx.get_node_attributes(G, 'name')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, labels=edge_labels)
    plt.savefig('graph.png')
    #print('\n' + str(len(final)) + " elementi nella lista.\n" + str(final))
    return final

