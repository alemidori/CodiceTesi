import lcs
import relations
import graph_relations
import itertools
import create_nyt_dataset

#todo: DA CAMBIARE TUTTO ********************************
#********************************
#********************************


def compose_methods():
    methodslist = ['lcs', 'relations', 'graph_relations']

    cursor = create_nyt_dataset.topicsecription.find()
    test = itertools.permutations(methodslist)
    configlist = list(test)

    for item in cursor:
        prov_stringlist = item['LDA_keywords']
        prov_specificlist = item['specific_words']
        for config in configlist:
            for met in config:
                if met == 'lcs':
                    prov_stringlist = lcs.process(prov_stringlist)
                    prov_specificlist = lcs.process(prov_specificlist)
                elif met == 'relations':
                    prov_stringlist = relations.process(prov_stringlist)
                    prov_specificlist = relations.process(prov_specificlist)
                elif met == 'graph_relations':
                    prov_stringlist = graph_relations.process(prov_stringlist)
                    prov_specificlist = graph_relations.process(prov_specificlist)
                else:
                    break
            stringconfig = str(config[0] + '-' + config[1] + '-' + config[2])
            stringconfigspecification = 'specificity-'+stringconfig
            item[stringconfig] = prov_stringlist
            item[stringconfigspecification] = prov_specificlist
            create_nyt_dataset.result_keywords.save(item)
    return




