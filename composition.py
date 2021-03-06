import lcs
import relations
import graph_relations
import supervised


class Composition:
    def __init__(self, stringlist, sequence):
        result = stringlist

        for item in sequence:
            if item == "lcs":
                result = lcs.process(result)
            elif item == "relations":
                result = relations.process(result)
            elif item == "graph_relations":
                result = graph_relations.process(result)
            else:
                print("Uno o più elementi inesistenti nella lista 'sequence'.")
        print("Risultato finale: "+str(result))

        return

