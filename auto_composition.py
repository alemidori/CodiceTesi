import lcs
import relations
import graph_relations
import itertools
import create_nyt_dataset

methodslist = ['lcs', 'relations', 'graph_relations']

#prendiamo i primi 10 record della collection results
stringlists = []
cursor = create_nyt_dataset.result_keywords.find().limit(10)
for elem in cursor:
    stringlists.append(elem['tokens'])

for it in stringlists:
    print(it)

test = itertools.permutations(methodslist)
configlist = list(test)
globdict = {}

for listitem in stringlists:
    print('Lista termini: '+str(listitem))
    provresult = listitem
    print(configlist)
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
        globdict[str(listitem)] = [config, provresult]

print(str(len(globdict)))
for k, v in globdict.items():
    print(k,v)
