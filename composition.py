import lcs
import relations
import graph_relations
import supervised


class Composition:
    def __init__(self, stringlist, sequence, similarity, numsynset):
        result = stringlist

        for item in sequence:
            if item == "lcs":
                result = lcs.process(result, similarity, numsynset)
            elif item == "relations":
                result = relations.process(result, similarity, numsynset)
            elif item == "graph_relations":
                result = graph_relations.process(result, similarity, numsynset)
            else:
                print("Uno o più elementi inesistenti nella lista 'sequence'.")
        print("Risultato finale: "+str(result))

        return

