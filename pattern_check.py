import sys
sys.setrecursionlimit(100000)
import manage_nyt_dataset
import strings_to_synsets
from nltk.corpus import wordnet as wn
import itertools

hyperstring = 'hypernym'
hypostring = 'hyponym'
holostring = 'holonym'
antostring = 'antonym'
globalpathslist = []

def process_paths():
    keywords = []
    hdpterms = []
    print('Produco le liste di keywords e termini hdp...')
    cursor = manage_nyt_dataset.topicsecription.find().limit(1)
    for record in cursor:
        for item in record['tuple_terms']:
            hdpterms.append(item[0])
        for item in record['merged_keywords_in_documents']:
            keywords.append(item[0])

    print('Ottengo tutti i synset per ogni keyword e per ogni termine hdp')
    keyword_group_synsets = []
    term_group_synsets = []
    for keyword in keywords:
        keyword_group_synsets.append([keyword, wn.synsets(keyword)])
    for term in hdpterms:
        term_group_synsets.append([term, wn.synsets(term)])
    # ho adesso i synset per entrambi i gruppi e devo verificarne i path:
    print('Synsets pronti.')
    compose_synsets(keyword_group_synsets, term_group_synsets)
    return


def compose_synsets(list_keywords_synsets, list_terms_synsets):
    pathslist = []
    for k in list_keywords_synsets:
        for t in list_terms_synsets:
            singlepath = []
            print('Produco le tuple tra synset per i termini k e t')
            tuples = list(itertools.product(k[1], t[1]))
            for tuple in tuples:
                singlepath.append(calculate_path(sk=tuple[0], st=tuple[1], jump=1, intersynsets=[], relationslist=[]))
            pathslist.append(singlepath)
            globalpathslist.append((k, t, pathslist))
    return


def calculate_path(sk, st, jump, intersynsets,
                   relationslist):  # sk = synset della keyword e st = synset del termine hdp
    path = []
    hypernyms = sk.hypernyms()
    hyponyms = sk.hyponyms()
    holonyms = sk.member_holonyms()
    antonyms = []
    intersynsets.append(sk)
    if sk.pos() == 'a':
        antonyms = sk.lemmas()[0].antonyms()
    if st in hypernyms:
        intersynsets.append(st)
        relationslist.append('hypernym')
        path = [intersynsets, relationslist, jump]
    elif st in hyponyms:
        intersynsets.append(st)
        relationslist.append('hyponym')
        path = [intersynsets, relationslist, jump]
    elif st in holonyms:
        intersynsets.append(st)
        relationslist.append('holonym')
        path = [intersynsets, relationslist, jump]
    elif antonyms and st in antonyms:
        intersynsets.append(st)
        relationslist.append('antonym')
        path = [intersynsets, relationslist, jump]
    else:
        iter_on = ''
        if len(relationslist) > 5:
            last_five_relations = [relationslist[i] for i in range(len(relationslist), len(relationslist) - 5)]
            if len(set(last_five_relations)) == 1:
                iter_on = list(set(last_five_relations))[0]

        if not iter_on or (iter_on and iter_on != hyperstring):
            for hyper in hypernyms:
                    relationslist.append(hyperstring)
                    calculate_path(hyper, st, jump + 1, intersynsets, relationslist)
        if not iter_on or (iter_on and iter_on != hypostring):
            for hypo in hyponyms:
                relationslist.append(hypostring)
                calculate_path(hypo, st, jump + 1, intersynsets, relationslist)

        if not iter_on or (iter_on and iter_on != holostring):
            for holo in holonyms:
                relationslist.append(holostring)
                calculate_path(holo, st, jump + 1, intersynsets, relationslist)

        if not iter_on or (iter_on and iter_on != antostring):
            if antonyms:
                for anto in antonyms:
                    relationslist.append(antostring)
                    calculate_path(anto, st, jump + 1, intersynsets, relationslist)

    return path

process_paths()
