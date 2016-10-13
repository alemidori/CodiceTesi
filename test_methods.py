import lcs
import relations
import graph_relations
import supervised
import test_lists
from composition import Composition
import sys

#print(lcs.process(example_list)) #test lcs
#print(relations.process(food_list50)) #test relations

#per liste molto lunghe nel graph_relations e' bene aumentare leggermente il parametro della similarita' per
#ridurre il numero di termini in output e quindi prendere un gruppo minore di nodi del grafo
#output1 =  graph_relations.process(food_list50, 0.2) #test graph_relations
#print(output1)
#print(lcs.process(['pasta', 'vegetable', 'yogurt', 'meat', 'cheese', 'butter', 'chocolate', 'beef', 'seafood', 'bread', 'pork', 'fish']))
#print(supervised.process(" ".join(food_list50)))

summary1 = ['relations', 'graph_relations'] #riassuntivo 1
summary2 = ['relations', 'lcs', 'graph_relations'] #riassuntivo 2
description1 = ['graph_relations', 'lcs', 'relations'] #descrittivo 1
description2 = ['lcs', 'graph_relations', 'relations'] #descrittivo 2

#param Composition > stringlist, sequenza, similarita' minima per coppie di termini, numero di synset massimi per un termine
composition = Composition(test_lists.food_list50, summary2, 0.3, 10)


#creare una funzione che permuta automaticamente i metodi generando tutte le possibili




