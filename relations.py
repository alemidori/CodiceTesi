from __future__ import division
import collections
import random
import lcs
import strings_to_synsets
import numpy as np
from nltk.corpus import wordnet as wn

final_list = []

def process(list_of_string):
    #print("\n\n*************INIZIO METODO RELATIONS")
    similarity = None
    flatten = lambda l: sum(map(flatten, l), []) if isinstance(l, list) else [l]
    set_string = list(set(flatten(list_of_string)))
    final_string = []
    # uso la funzione di lcs string_to_synsets(considerando anche aggettivi avverbi e verbi)
    # per ottenere i synsets dalla lista dei termini in input
    synsetslist = strings_to_synsets.get_all_synsets(set_string)
    #print("I synset sono: " + str(len(synsetslist)))
    #print(synsetslist)

    for i in range(0, (len(synsetslist) - 1)):
        for j in range(i + 1, (len(synsetslist) - 1)):
            check_relation(synsetslist[i], synsetslist[j])

    set_final = []
    [set_final.append(item) for item in final_list if item not in set_final]

    for synset in set_final:
        final_string.append(synset.lemmas()[0].name())
    final_string_set = []
    [final_string_set.append(item) for item in final_string if item not in final_string_set]

    #print('\n'+str(len(final_string_set))+" elementi nella lista.\n" + str(final_string_set))
    if not final_string_set:
        print("Sono stati scartati tutti i termini perché aventi più synset del parametro impostato. ("+ str(10)+")")
    return final_string_set


def check_relation(sy1, sy2):
    global final_list
    #verifica relazione di iperonimia
    if sy1.max_depth() > sy2.max_depth():
        #print(str(sy2)+" più generico di "+str(sy1))
        final_list.append(sy2)
    elif sy1.max_depth() < sy2.max_depth():
        #print(str(sy1) + " più generico di " + str(sy2))
        final_list.append(sy1)

    #se il grado nel grafo è uguale si verifica se sono sinonimi
    else:
        #print("***Sono allo stesso livello nel grafo")
        synlist = [sy1, sy2]
        synon_list1 = sy1.hypernyms() #lista dei sinonimi di sy1
        synon_list2 = sy2.hypernyms()  # lista dei sinonimi di sy2
        if sy2 in synon_list1 or sy1 in synon_list2: #se uno si trova nella lista dell'altro
            #print("////Sono sinonimi")
            final_list.append(random.choice(synlist)) #scegli random uno dei due

    #se sono contrari (un synset può avere contrari solo se è un aggettivo)
    if sy1.pos() == 'a' and sy2.pos() == 'a':
        if sy2 in sy1.lemmas()[0].antonyms() or sy1 in sy2.lemmas()[0].antonyms():
            #print("----Sono contrari")
            final_list.append(sy1) #appendi entrambi alla lista
            final_list.append(sy2)
    return






