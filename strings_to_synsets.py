from nltk.corpus import wordnet as wn
flatten = lambda l: sum(map(flatten, l), []) if isinstance(l, list) else [l]

def get_noun_synsets(strings, param):
    synsetslist = []
    for term in flatten(strings):
        if len(wn.synsets(term)) <= param:  # scarto i termini che hanno piu' di 10 significati
            for synset in wn.synsets(term):
                if synset.pos() == 'n':
                    synsetslist.append(
                        synset)  # inserisco in un'unica lista tutti i synset dei termini per poi confrontarli
    return synsetslist

def get_all_synsets(strings, param):
    synsetslist = []
    for term in flatten(strings):
        if len(wn.synsets(term)) <= param:  # scarto i termini che hanno piu' di 10 significati
            for synset in wn.synsets(term):
                if synset.pos() == 'n':
                    synsetslist.append(
                        synset)  # inserisco in un'unica lista tutti i synset dei termini per poi confrontarli
    return synsetslist