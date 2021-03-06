import networkx as nx
import nltk
from nltk.corpus import wordnet as wn
import time

source_synsets = []
target_synsets = []
global_syn = []
source_synsets_list = []
target_synsets_list = []
G = nx.Graph()
mark_syn = []


def check_path(source, target, filename):
    # elimino TUTTI i termini marcati perchè è un NUOVO grafo!!!
    # mark_syn.clear()
    print('TERMINI: ' + str(source) + ', ' + str(target))
    print('Estraggo i synset per i termini...')
    # uso le variabili globali per passare gli argomenti alle altre funzioni
    global source_synsets
    global target_synsets
    # setto le variabili con i synsets corretti
    source_synsets = wn.synsets(source)
    target_synsets = wn.synsets(target)
    if source_synsets and target_synsets:
        print(source_synsets)
        print(target_synsets)
        # aggiungo i nodi iniziali nel grafo
        for synset in source_synsets:
            G.add_node(synset, name=synset.lemmas()[0].name())
            print('Aggiungo nodo ' + str(synset))
        for synset in target_synsets:
            G.add_node(synset, name=synset.lemmas()[0].name())
            print('Aggiungo nodo ' + str(synset))

        find_path = False

        # for source_synset in source_synsets:
        #     for target_synset in target_synsets:
        #         if nx.has_path(G, source_synset, target_synset):
        #             booleanvalue = True
        # while not nx.has_path(G, source_synset, target_synset):
        # expand(G)
        # print('Esiste un path tra il synset source: '+ str(source_synset) +' e: '+str(target_synset))
        counter = 0
        while find_path == False and counter < 10:
            find_path = verify_connection(filename)
            counter += 1
        if find_path == False and counter == 10:
            write_file(source, target, [], 'None', '-1',  filename)
            print('Troppe espansioni. Termino il processo.')
        print(G.number_of_nodes())
    else:
        print('Una delle liste di synset è vuota.')
        if not source_synsets:
            write_file(source, target, [], 'None', 'None', filename)
        if not target_synsets:
            write_file(source, target, [], 'None', 'None', filename)

    # print('Disegno il grafo...')
    # pos = nx.spring_layout(G, scale=2)
    # nx.draw(G, pos)
    # node_labels = nx.get_node_attributes(G, 'name')
    # nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
    # plt.savefig('path_graph.png')
    return


def verify_connection(filename):
    global G
    for source_synset in source_synsets:
        for target_synset in target_synsets:
            if nx.has_path(G, source_synset, target_synset):
                relations = []
                print('TROVATO PERCORSO')
                shortest_path = (list(nx.shortest_path(G, source=source_synset, target=target_synset)))
                print("SHORTEST PATH:" + str(shortest_path))
                for i in range(0, len(shortest_path) - 1):
                    relations.append(list(G.get_edge_data(shortest_path[i], shortest_path[i + 1]).values()))
                    print('Labels Archi ' + str(shortest_path[i]) + ' - ' + str(shortest_path[i + 1]) + ': ' + str(
                        list(G.get_edge_data(shortest_path[i], shortest_path[i + 1]).values())))

                write_file(source_synset.lemmas()[0].name(), target_synset.lemmas()[0].name(), sum(relations, []),
                           shortest_path, len(relations), filename)
                return True

    print('Non trovate connessioni, espando il grafo.')
    gaptime = expand()
    print('GAPTIME: ' + str(gaptime))

    return False


def expand():
    global G
    gaptime = 0.0
    start = time.time()
    for node in G.nodes():
        if (node not in mark_syn) and (node not in target_synsets):
            expansion(node)
        gaptime = time.time() - start
        if gaptime > float(10.0):  # se ci metto piu' di 20 secondi termino l'espansione
            return gaptime
    return gaptime


def expansion(synset):
    mark_syn.append(synset)  # marko il nodo perché lo sto aggiungendo al grafo

    if synset not in G.nodes():
        G.add_node(synset, name=synset.lemmas()[0].name())

    hypernyms = synset.hypernyms()
    hyponyms = synset.hyponyms()
    hyponyms = hyponyms[:5]
    holonyms = synset.member_holonyms()
    if isinstance(synset, nltk.corpus.reader.wordnet.Synset):
        if synset.pos() == 'a':
            antonyms = synset.lemmas()[0].antonyms()
            for anto in antonyms:
                G.add_node(anto, name=anto.name())
                if not G.has_edge(synset, anto):
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
        if not G.has_edge(synset, holo):
            G.add_edge(synset, holo, label='holonym')
    return


def write_file(source, target, relations, synsets, expansions, filename):
    with open(filename + '.tsv', 'a') as file:
        file.write(source + '\t' + target + '\t' + str(relations) + '\t' + str(synsets) + '\t' + str(expansions))
        file.write("\n")
        file.close()
    return
