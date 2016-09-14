from nltk.corpus import wordnet as wn
from nltk import tag

final = []

def process(list_of_string):
    lcs_list = []
    synsetslist = []
    terms_dict = {}
    set_string = []
    terms_synsets_list = []
    nouns_synset_list = []
    [set_string.append(item) for item in list_of_string if item not in set_string]
    if len(set_string) > 1:
        for term in set_string:
            if len(wn.synsets(term)) <= 10: #scarto i termini che hanno piu' di 10 significati
                for synset in wn.synsets(term):
                    if synset.pos() == 'n':
                        synsetslist.append(synset) # inserisco in un'unica lista tutti i synset dei termini per poi confrontarli


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

        more_similar_couple = {}

        for key in terms_dict.keys():
            if key >= 0.15:
                more_similar_couple[key] = terms_dict[key]

        if more_similar_couple:
            lcs_list.clear()
            for key in more_similar_couple.keys():
                lcs_list.append(more_similar_couple[key][2])

        else:
            lcs_list.clear()
            for key in terms_dict.keys():
                lcs_list.append(terms_dict[key][2])

        lcs_set = []
        [lcs_set.append(item) for item in lcs_list if item not in lcs_set]

        new_list_of_string = []

        lcs_set = sum(lcs_set, [])
        for synset in lcs_set:
            new_list_of_string.append(synset.lemmas()[0].name())

        if new_list_of_string:
            final.clear()
            [final.append(item) for item in new_list_of_string if item not in final]

        if more_similar_couple:
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


