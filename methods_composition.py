import lcs
import relations
import graph_relations
import itertools
import manage_nyt_dataset

def compose_methods():
    methodslist = ['lcs', 'relations', 'graph_relations']

    cursor = manage_nyt_dataset.topicsecription.find()
    test = itertools.permutations(methodslist)
    configlist = list(test)

    incr = 0
    for item in cursor:
        tuple_hdp = []
        tuple_specificity = []
        for k in item['tuple_terms']:
            tuple_hdp.append((k[0], 0)) #costruisco tante tuple quanti sono i termini di hdp (ossia 10) con peso = 0
        for j in item['specific_words_in_documents']:
            tuple_specificity.append((j, 0)) #costruisco tante tuple quanti sono i termini specifici nei docs con peso 0
        for config in configlist:
            for met in config:
                if met == 'lcs':
                    tuple_hdp = lcs.process(tuple_hdp)
                    tuple_specificity = lcs.process(tuple_specificity)
                elif met == 'relations':
                    tuple_hdp = relations.process(tuple_hdp)
                    tuple_specificity = relations.process(tuple_specificity)
                elif met == 'graph_relations':
                    tuple_hdp = graph_relations.process(tuple_hdp)
                    tuple_specificity = graph_relations.process(tuple_specificity)
                else:
                    break
            stringconfig = str(config[0] + '-' + config[1] + '-' + config[2])
            stringconfigspecification = 'SPECIFICITY-'+stringconfig
            item[stringconfig] = tuple_hdp
            item[stringconfigspecification] = tuple_specificity
            manage_nyt_dataset.topicsecription.save(item)
        incr += 1
    return




