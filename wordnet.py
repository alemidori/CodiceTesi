from nltk.corpus import wordnet as wn
from nltk.corpus import genesis

#identifichiamo i termini come sostantivo, aggettivi, verbi e avverbi presenti in wordnet usando synset
#n = sostantivo, v = verbo, a = aggettivo,
dog = wn.synset('dog.n.01')
cat = wn.synset('cat.n.01')
good = wn.synset('good.a.01')

#print(dog.path_similarity(cat))

genesis_ic = wn.ic(genesis, False, 0.0)
#print(dog.res_similarity(cat, genesis_ic)) #similarita' calcolata in base al contenuto informativo fornito (in questo caso la genesi)

# for synset in wn.synsets('dog'):
#     for lemma in synset.lemmas():
#         print(lemma.name())


