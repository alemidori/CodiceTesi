import networkx as nx
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt

source_synsets = []
target_synsets = []
global_syn = []
source_synsets_list = []
target_synsets_list = []
G = nx.Graph()

mark_syn = []

def check_path(source, target):
    print('Estraggo i synset per i termini...')
    # uso le variabili globali per passare gli argomenti alle altre funzioni
    global source_synsets
    global target_synsets
    # setto le variabili con i synsets corretti
    source_synsets = wn.synsets(source)
    target_synsets = wn.synsets(target)

    print(source_synsets)
    print(target_synsets)
    # aggiungo i nodi iniziali nel grafo
    for synset in source_synsets:
        G.add_node(synset, name=synset.lemmas()[0].name())
        print ('Aggiungo nodo ' + str(synset))
    for synset in target_synsets:
        G.add_node(synset, name=synset.lemmas()[0].name())
        print ('Aggiungo nodo ' + str(synset))

    find_path = False

    # for source_synset in source_synsets:
    #     for target_synset in target_synsets:
    #         if nx.has_path(G, source_synset, target_synset):
    #             booleanvalue = True
            #while not nx.has_path(G, source_synset, target_synset):
                #expand(G)
            #print('Esiste un path tra il synset source: '+ str(source_synset) +' e: '+str(target_synset))

    while find_path == False:
        find_path = verify_connection()


    # print('Disegno il grafo...')
    # pos = nx.spring_layout(G, scale=2)
    # nx.draw(G, pos)
    # node_labels = nx.get_node_attributes(G, 'name')
    # nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
    # plt.savefig('path_graph.png')
    return


def verify_connection():
    for source_synset in source_synsets:
        for target_synset in target_synsets:
            if nx.has_path(G, source_synset, target_synset):
                print('TROVATO PERCORSO')
                shortest_path = (list(nx.shortest_path(G, source=source_synset, target=target_synset)))
                print ("SHORTEST PATH:" + str(shortest_path))
                for i in range(0, len(shortest_path) -1):
                        print('Labels Archi '+str(shortest_path[i])+' - '+str(shortest_path[i+1])+': '
                              +str(list(G.get_edge_data(shortest_path[i], shortest_path[i+1]).values())))
                return True
    print ('Non trovate connessioni, espando il grafo.')
    expand()
    return False

def expand():
    for node in G.nodes():
        if (node not in mark_syn) and (node not in target_synsets):
            expansion(node)
    return

def expansion(synset):
    print ('Espansione nodo ' + str(synset))
    mark_syn.append(synset)

    if synset not in G.nodes():
        G.add_node(synset, name=synset.lemmas()[0].name())

    hypernyms = synset.hypernyms()
    hyponyms = synset.hyponyms()
    holonyms = synset.member_holonyms()

    if synset.pos() == 'a':
        antonyms = synset.lemmas()[0].antonyms()
        for anto in antonyms:
            G.add_node(anto, name=anto.lemmas()[0].name())
            if not G.has_edge(synset,anto):
                G.add_edge(synset, anto, label='antonym')
    for hyper in hypernyms:
        G.add_node(hyper, name=hyper.lemmas()[0].name())
        if not G.has_edge(synset, hyper):
            G.add_edge(synset, hyper, label='hypernym')
    for hypo in hyponyms:
        G.add_node(hypo, name=hypo.lemmas()[0].name())
        if not G.has_edge(synset, hypo):
            G.add_edge(synset, hypo, label='hyponym')
    for holo in holonyms:
        G.add_node(holo, name=holo.lemmas()[0].name())
        if not G.has_edge(synset,holo):
            G.add_edge(synset, holo, label='holonym')

    return

check_path('person','milk')
#check_path('politics', 'say')