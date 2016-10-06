from nltk.corpus import wordnet as wn
import strings_to_synsets
from nltk import tag

final = []

def process(list_of_string):
    lcs_list = []
    terms_dict = {}
    set_string = list(set(list_of_string))
    #terms_synsets_list = []
    #nouns_synset_list = []

    if len(set_string) > 1:
        synsetslist = strings_to_synsets.get_noun_synsets(set_string)

        # [terms_synsets_list.append(synset.lemmas()[0].name()) for synset in synsetslist]
        # returned_list = tag_terms(terms_synsets_list)
        # synsetslist.clear()
        # [synsetslist.append(wn.synsets(term)) for term in returned_list]
        # synsetslist = sum(synsetslist, [])
        # print(synsetslist)
        #
        # for synset in synsetslist:
        #     if synset.pos() == 'n':
        #         nouns_synset_list.append(synset)
        #
        # for i in range(0, (len(nouns_synset_list)-1)):
        #     for j in range(i+1, (len(nouns_synset_list)-1)):
        #         score = nouns_synset_list[i].path_similarity(nouns_synset_list[j])
        #         lcs = nouns_synset_list[i].lowest_common_hypernyms(nouns_synset_list[j])
        #         #dict: chiave: score, valore: [termine1, termine2, lcs]
        #         terms_dict[score] = [nouns_synset_list[i], nouns_synset_list[j], lcs]
        #         lcs_list.append(lcs)

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

        if len(more_similar_couples) > 1:
            lcs_list.clear()
            for key in more_similar_couples.keys():
                lcs_list.append(more_similar_couples[key][2])

        else:
            lcs_list.clear()
            for key in terms_dict.keys():
                lcs_list.append(terms_dict[key][2])

        lcs_set = list(set(lcs_list))

        new_list_of_string = []

        lcs_set = sum(lcs_set, [])
        print(lcs_set)

        setforremove = lcs_set

        for synset in setforremove:
            #evito di considerare termini come: entita', entita' fisica ecc, quindi troppo generici
            #verifico dunque il livello di profondita' (0 = entity)
            if synset.max_depth() < 3:
                print(str(synset)+" --> "+str(synset.max_depth()))
                print(str(synset)+" troppo generica")
                lcs_set.remove(synset)


        for synset in lcs_set:
            print(synset)
            new_list_of_string.append(synset.lemmas()[0].name())

        if new_list_of_string:
            global final
            final.clear()
            final = list(set(new_list_of_string))

        if len(more_similar_couples) > 1:
            process(new_list_of_string)

    #se la lista iniziale e' composta da un solo termine, stampa quello
    else:
        final.append(list_of_string)


    return final


def tag_terms(list_of_terms):
    list_nouns = []
    print(list_of_terms)
    tuple_list = tag.pos_tag(list_of_terms)
    [list_nouns.append(term[0]) for term in tuple_list if term[1] == 'NN']

    print(list_nouns)
    return list_nouns



#non posso calcolare la path similarity indifferentemente tra sostantivi, verbi, aggettivi e avverbi
#quindi una volta taggati i termini con tag_terms procedo al calcolo della similarità usando path similarity solo tra nouns

#nltk.tag (modulo) da applicare prima
#scopus (database bibliografico) (banca dati unimi)


