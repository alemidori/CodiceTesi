import sys
import manage_nyt_dataset
import strings_to_synsets
from nltk.corpus import wordnet as wn
import itertools
import pattern_check_networkx

hyperstring = 'hypernym'
hypostring = 'hyponym'
holostring = 'holonym'
antostring = 'antonym'
globalpathslist = []
variable = False


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

    tuples = list(set(itertools.product(hdpterms, keywords)))
    print(tuples)

#     print('Ottengo tutti i synset per ogni keyword e per ogni termine hdp')
#     keyword_group_synsets = []
#     term_group_synsets = []
#     for keyword in keywords:
#         keyword_group_synsets.append([keyword, wn.synsets(keyword)])
#     for term in hdpterms:
#         term_group_synsets.append([term, wn.synsets(term)])
#     # ho adesso i synset per entrambi i gruppi e devo verificarne i path:
#     print('Synsets pronti.')
#     compose_synsets(keyword_group_synsets, term_group_synsets)
#     return
#
#
# def compose_synsets(list_keywords_synsets, list_terms_synsets):
#     tuples = list(itertools.product(list_keywords_synsets[0][1], list_terms_synsets[0][1]))
#     print(tuples[0][0])
#     print(tuples[0][1])
#     dog = wn.synset('dog.n.01')
#     canine = wn.synset('dog.n.01').hypernyms()[0]
#     carivore = canine.hypernyms()[0]
#     # print(calculate_path(sk=tuples[0][0], st=tuples[0][1], jump=1, intersynsets=[], relationslist=[], marked=[]))
#     #print(calculate_path_2(sk=tuples[0][0], st=tuples[0][1]))
#
#     #print (calculate_path_2(canine,carivore))
#     # pathslist = []
#     # for k in list_keywords_synsets:
#     #     for t in list_terms_synsets:
#     #         singlepath = []
#     #         print('Produco le tuple tra synset per i termini k e t')
#     #         tuples = list(itertools.product(k[1], t[1]))
#     #         for tuple in tuples:
#     #             singlepath.append(calculate_path(sk=tuple[0], st=tuple[1], jump=1, intersynsets=[], relationslist=[], marked=[]))
#     #         pathslist.append(singlepath)
#     #         print(pathslist)
#     #         globalpathslist.append((k, t, pathslist))
#     return
#
#
# def calculate_path(sk, st, jump, intersynsets,
#                    relationslist, marked):  # sk = synset della keyword e st = synset del termine hdp
#     hypernyms = sk.hypernyms()
#     hyponyms = sk.hyponyms()
#     holonyms = sk.member_holonyms()
#     antonyms = []
#     print(sk, st)
#     intersynsets.append(sk)
#     if sk.pos() == 'a':
#         antonyms = sk.lemmas()[0].antonyms()
#     if st in hypernyms:
#         intersynsets.append(st)
#         relationslist.append('hypernym')
#         path = [intersynsets, relationslist, jump]
#         return True, path
#     elif st in hyponyms:
#         intersynsets.append(st)
#         relationslist.append('hyponym')
#         path = [intersynsets, relationslist, jump]
#         return True, path
#     elif st in holonyms:
#         intersynsets.append(st)
#         relationslist.append('holonym')
#         path = [intersynsets, relationslist, jump]
#         return True, path
#     elif antonyms and st in antonyms:
#         intersynsets.append(st)
#         relationslist.append('antonym')
#         path = [intersynsets, relationslist, jump]
#         return True, path
#     else:
#         iter_on = ''
#         if len(relationslist) > 5:
#             print(relationslist)
#             print(len(relationslist))
#             last_five_relations = [relationslist[i] for i in range(len(relationslist) - 5, len(relationslist))]
#             print(last_five_relations)
#             if len(set(last_five_relations)) == 1:
#                 print('SET DI RELATIONS')
#                 iter_on = list(set(last_five_relations))[0]
#         if not iter_on or (iter_on and iter_on != hyperstring):
#             print('ENTRO IN HYPER')
#             for hyper in hypernyms:
#                 print('hypernyms ' + str(hypernyms))
#                 if hyper not in marked:
#                     print('non marcato ' + str(hyper))
#                     relationslist.append(hyperstring)
#                     marked.append(hyper)
#                     try:
#                         result, path = calculate_path(hyper, st, jump + 1, intersynsets, relationslist, marked)
#                         if result:
#                             return True, path
#                     except TypeError:
#                         print('vado avanti')
#         if not iter_on or (iter_on and iter_on != hypostring):
#             for hypo in hyponyms:
#                 print('hyponyms ' + str(hyponyms))
#                 if hypo not in marked:
#                     print('non marcato ' + str(hypo))
#                     relationslist.append(hypostring)
#                     marked.append(hypo)
#                     print(hypo, st, jump, intersynsets, relationslist, marked)
#                     try:
#                         result, path = calculate_path(hypo, st, jump + 1, intersynsets, relationslist, marked)
#                         if result:
#                             return True, path
#                     except TypeError:
#                         print('vado avanti')
#         if not iter_on or (iter_on and iter_on != holostring):
#             for holo in holonyms:
#                 if holo not in marked:
#                     relationslist.append(holostring)
#                     marked.append(holo)
#                     try:
#                         result, path = calculate_path(holo, st, jump + 1, intersynsets, relationslist, marked)
#                         if result:
#                             return True, path
#                     except TypeError:
#                         print('vado avanti')
#         if not iter_on or (iter_on and iter_on != antostring):
#             if antonyms:
#                 for anto in antonyms:
#                     if anto not in marked:
#                         relationslist.append(antostring)
#                         marked.append(anto)
#                         try:
#                             result, path = calculate_path(anto, st, jump + 1, intersynsets, relationslist, marked)
#                             if result:
#                                 return True, path
#                         except TypeError:
#                             print('vado avanti')
#
#
# def verifyRelationList(relationslist):
#     iter_on = ''
#     # verifico la lunghezza della relationslist
#     if len(relationslist) > 5:
#         print('Sono presenti più di 5 relazioni; analizzo se sono uguali.')
#         last_five_relations = [relationslist[i] for i in range(len(relationslist) - 5, len(relationslist))]
#         if (len(set(last_five_relations)) == 1):
#             print('Ultime 5 relazioni tutte uguali, switcho la relazione')
#             iter_on = list(set(last_five_relations))[0]
#     return iter_on
#
# def calculate_path_2(sk, st):  # sk = synset della keyword e st = synset del termine hdp
#
#     first_synset = sk
#     second_synset = st
#
#     previous_first_synset = ''
#
#     marked_synset = {}
#     jump = 1
#     intersynsets = []
#     relationslist = []
#     path = []
#     print(first_synset, second_synset)
#     intersynsets.append(first_synset)
#
#     while not path:
#         print("FIRST SYNSET " + str(first_synset))
#         print("SECOND SYNSET " + str(second_synset))
#         print("RELATION LIST " + str(relationslist))
#
#         # tengo traccia del precedente
#         try:
#             previous_first_synset = marked_synset[first_synset]
#         except KeyError:
#             print('Primo giro')
#
#         hypernyms = first_synset.hypernyms()
#         hyponyms = first_synset.hyponyms()
#         holonyms = first_synset.member_holonyms()
#         antonyms = []
#
#         if first_synset.pos() == 'a':
#             antonyms = first_synset.lemmas()[0].antonyms()
#
#         if second_synset in hypernyms:
#             intersynsets.append(second_synset)
#             relationslist.append('hypernym')
#             path = [intersynsets, relationslist, jump]
#         elif second_synset in hyponyms:
#             intersynsets.append(second_synset)
#             relationslist.append('hyponym')
#             path = [intersynsets, relationslist, jump]
#         elif second_synset in holonyms:
#             intersynsets.append(second_synset)
#             relationslist.append('holonym')
#             path = [intersynsets, relationslist, jump]
#         elif antonyms and second_synset in antonyms:
#             intersynsets.append(second_synset)
#             relationslist.append('antonym')
#             path = [intersynsets, relationslist, jump]
#         else:
#             # lungh. relazione
#             iter_on = verifyRelationList(relationslist)
#
#             if (iter_on != hyperstring) and (first_synset != wn.synset('entity.n.01')):
#                 print('Entro in hyper')
#                 found_not_mark = False
#                 for item in hypernyms:
#                     if item not in marked_synset.keys():
#                         found_not_mark = True
#                         print(str(item) + ' non marcato, analizzo')
#                         # salvo il precedente nel dizionario
#                         marked_synset[item] = first_synset
#                         # item diventa il primo synset
#                         first_synset = item
#                         # aumento il jump
#                         jump += 1
#                         # appendo la relazione utilizzata
#                         relationslist.append(hyperstring)
#                         intersynsets.append(item)
#                         break
#
#                 if found_not_mark == False:
#                     # devo verificare tutto il resto
#                     print('Devo verificare i restanti metodi; inizio con Hypo')
#                     print('Entro in hypo')
#                     for item in hyponyms:
#                         if item not in marked_synset.keys():
#                             found_not_mark = True
#                             print(str(item) + ' non marcato, analizzo')
#                             # salvo il genitore nel dizionario
#                             marked_synset[item] = first_synset
#                             # item diventa il primo synset
#                             first_synset = item
#                             # aumento il jump
#                             jump += 1
#                             # appendo la relazione utilizzata
#                             relationslist.append(hypostring)
#                             intersynsets.append(item)
#                             break
#
#                 if found_not_mark == False:
#                     print('Continuo a verificare con Holo')
#                     print('Entro in holo')
#                     for item in holonyms:
#                         if item not in marked_synset.keys():
#                             found_not_mark = True
#                             print(str(item) + ' non marcato, analizzo')
#                             # salvo il genitore nel dizionario
#                             marked_synset[item] = first_synset
#                             # item diventa il primo synset
#                             first_synset = item
#                             # aumento il jump
#                             jump += 1
#                             # appendo la relazione utilizzata
#                             relationslist.append(holostring)
#                             intersynsets.append(item)
#                             break
#
#                 if found_not_mark == False:
#                     print('Verifico infine Anto')
#                     for item in antonyms:
#                         if item not in marked_synset.keys():
#                             found_not_mark = True
#                             # salvo il genitore nel dizionario
#                             marked_synset[item] = first_synset
#                             # item diventa il primo synset
#                             first_synset = item
#                             # aumento il jump
#                             jump += 1
#                             # appendo la relazione utilizzata
#                             relationslist.append(antostring)
#                             intersynsets.append(item)
#                             break
#
#                 if found_not_mark == False:
#                     # non mi e' stato ritrovato nulla, finisco con questo synset e considero il precedente
#                     print('Tutti marcati, setto quello precedente')
#                     first_synset = previous_first_synset
#             else:
#                 if iter_on != hypostring:
#                     print('Entro in hypo')
#                     print (hyponyms)
#                     found_not_mark_hypo = False
#                     for item in hyponyms:
#                         if item not in marked_synset.keys():
#                             found_not_mark_hypo = True
#                             print(str(item) + ' non marcato, analizzo')
#                             # salvo il genitore nel dizionario
#                             marked_synset[item] = first_synset
#                             # item diventa il primo synset
#                             first_synset = item
#                             # aumento il jump
#                             jump += 1
#                             # appendo la relazione utilizzata
#                             relationslist.append(hypostring)
#                             intersynsets.append(item)
#                             break
#                     if found_not_mark_hypo == False:
#                         print('Tutti marcati, setto quello precedente')
#                         first_synset = previous_first_synset
#                 else:
#                     if iter_on != holostring:
#                         print('Entro in holo')
#                         found_not_mark_holo = False
#                         for item in holonyms:
#                             if item not in marked_synset.keys():
#                                 found_not_mark_holo = True
#                                 print(str(item) + ' non marcato, analizzo')
#                                 # salvo il genitore nel dizionario
#                                 marked_synset[item] = first_synset
#                                 # item diventa il primo synset
#                                 first_synset = item
#                                 # aumento il jump
#                                 jump += 1
#                                 # appendo la relazione utilizzata
#                                 relationslist.append(holostring)
#                                 intersynsets.append(item)
#                                 break
#                         if found_not_mark_holo == False:
#                             print('Tutti marcati, setto quello precedente')
#                             first_synset = previous_first_synset
#                     else:
#                         if (iter_on != antostring) and antonyms:
#                             print('Entro in anto')
#                             found_not_mark_anto = False
#                             for item in antonyms:
#                                 if item not in marked_synset.keys():
#                                     found_not_mark_anto = True
#                                     # salvo il genitore nel dizionario
#                                     marked_synset[item] = first_synset
#                                     # item diventa il primo synset
#                                     first_synset = item
#                                     # aumento il jump
#                                     jump += 1
#                                     # appendo la relazione utilizzata
#                                     relationslist.append(antostring)
#                                     intersynsets.append(item)
#                                     break
#                             if found_not_mark_anto == False:
#                                 print('Tutti marcati, setto quello precedente')
#                                 first_synset = previous_first_synset
#
#     return path



#process_paths()
#print(calculate_path_2(wn.synset('dog.n.01'), wn.synset('carnivore.n.01')))

process_paths()