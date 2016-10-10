import lcs
import relations
import graph_relations
import supervised


class Composition:
    def __init__(self, stringlist, sequence, similarity):
        result = stringlist

        for item in sequence:
            if item == "lcs":
                result = lcs.process(result, similarity)
            elif item == "relations":
                result = relations.process(result, similarity)
            elif item == "graph_relations":
                result = graph_relations.process(result, similarity)
            elif item == "supervised":
                result = supervised.process(result, similarity)
            else:
                print("Uno o più elementi inesistenti nella lista 'sequence'.")
        print(result)

        return

