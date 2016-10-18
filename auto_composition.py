import lcs
import relations
import graph_relations
import itertools
import create_nyt_dataset
import specificity_nyt

methodslist = ['lcs', 'relations', 'graph_relations']

def compose_methods():
    # prendiamo i primi tot record della collection results
    stringlists = []
    cursor = create_nyt_dataset.result_keywords.find()
    for elem in cursor:
        stringlists.append(elem['tokens'])

    test = itertools.permutations(methodslist)
    configlist = list(test)
    globlist = []

    increment = 0
    for listitem in stringlists:
        print('___________________________Lista termini '+str(increment)+' :'+str(listitem))
        provresult = listitem
        #print(configlist)
        for config in configlist:
            print('Configurazione: '+str(config))
            for met in config:
                if met == 'lcs':
                    provresult = lcs.process(provresult)
                elif met == 'relations':
                    provresult = relations.process(provresult)
                elif met == 'graph_relations':
                    provresult = graph_relations.process(provresult)
                else:
                    print("Uno o più metodi inesistenti nella lista 'globlist'.")
            print("Risultato finale configurazione: " + str(provresult)+ '\n')

            stringconfig = str(config[0]+'-'+config[1]+'-'+config[2])
            update_collection(listitem, stringconfig, provresult)
            #globlist.append([listitem, config, provresult])
        increment += 1

    # for conflist in globlist:
    #     print("Lista: " + str(conflist[0]) + " Configurazione: " + str(conflist[1]) + " Risultato: " + str(conflist[2]))
    # return globlist

def add_specific_words_to_collection():
    cursor = create_nyt_dataset.result_keywords.find()
    for element in cursor:
        ldawords = element['LDA_keywords']
        tokens = element['tokens']
        specificwords = specificity_nyt.get_specific_words(ldawords, tokens)
        element['specific_words'] = specificwords
        create_nyt_dataset.result_keywords.save(element)
    return


def update_collection(tokenlist, configuration, configresult):
    cursor = create_nyt_dataset.result_keywords.find({'tokens': tokenlist})
    for elem in cursor:
        elem[configuration] = configresult
        create_nyt_dataset.result_keywords.save(elem)
    return

add_specific_words_to_collection()
#compose_methods()
