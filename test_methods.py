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

summary1 = ['lcs', 'relations', 'graph_relations']
summary2 = ['relations', 'lcs', 'graph_relations']
description1 = ['graph_relations', 'lcs', 'relations']
description2 = ['lcs', 'graph_relations', 'relations']

#param Composition > stringlist, sequence, similarity
composition = Composition(test_lists.abstract, summary1, 0.2)



