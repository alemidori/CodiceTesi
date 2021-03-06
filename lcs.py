from nltk.corpus import wordnet as wn
import strings_to_synsets

final = []

def process(tuples):
    print("\n\n*************INIZIO METODO LCS")
    flatten = lambda l: sum(map(flatten, l), []) if isinstance(l, list) else [l]
    tuples = flatten(tuples)
    print(tuples)
    lcs_list = []
    terms_dict = {}
    set_string = []

    for t in tuples:
        set_string.append(t[0])
    set_string = list(set(set_string))
    #terms_synsets_list = []
    #nouns_synset_list = []
    final_tuples = []

    if len(set_string) > 1:
        synsetslist = strings_to_synsets.get_noun_synsets(set_string)
        print(set_string)
        print(synsetslist)
        for i in range(0, (len(synsetslist) - 1)):
            for j in range(i+1, (len(synsetslist)-1)):
                score = synsetslist[i].path_similarity(synsetslist[j])
                lcs = synsetslist[i].lowest_common_hypernyms(synsetslist[j])
                #dict: chiave: score, valore: [termine1, termine2, lcs]
                terms_dict[score] = [synsetslist[i], synsetslist[j], lcs]
                lcs_list.append(lcs)

        more_similar_couples = {}

        for key in terms_dict.keys():
            if key >= 0.3:
                more_similar_couples[key] = terms_dict[key]

        if len(more_similar_couples) > 2:
            lcs_list.clear()
            for key in more_similar_couples.keys():
                lcs_list.append(more_similar_couples[key][2])

        else:
            lcs_list.clear()
            for key in terms_dict.keys():
                lcs_list.append(terms_dict[key][2])

        lcs_list = sum(lcs_list, [])
        lcs_set = list(set(lcs_list))
        #print(lcs_set)

        new_list_of_string = []

        setforremove = lcs_set

        for synset in setforremove:
            #evito di considerare termini come: entita', entita' fisica ecc, quindi troppo generici
            #verifico dunque il livello di profondita' (0 = entity)
            if synset.max_depth() < 3:
                #print(str(synset)+" --> "+str(synset.max_depth()))
                #print(str(synset)+" troppo generica")
                lcs_set.remove(synset)


        for synset in lcs_set:
            #print(synset)
            new_list_of_string.append(synset.lemmas()[0].name())

        if new_list_of_string:
            global final
            final.clear()
            final = list(set(new_list_of_string))
            for f in final:
                final_tuples.append((f, 0))

        if len(more_similar_couples) > 2:
            #print('\n' + str(final))
            recors_tuples = []
            for n in new_list_of_string:
                recors_tuples.append((n, 0))
            process(recors_tuples)


    #se la lista iniziale e' composta da un solo termine, stampa quello
    else:
        for t in tuples:
            final_tuples.append(t)

    #print('\n' + str(len(final)) + " elementi nella lista.\n" + str(flatten(final)))
    return final_tuples



#non posso calcolare la path similarity indifferentemente tra sostantivi, verbi, aggettivi e avverbi
#quindi una volta taggati i termini con tag_terms procedo al calcolo della similarità usando path similarity solo tra nouns

#nltk.tag (modulo) da applicare prima
#scopus (database bibliografico) (banca dati unimi)


