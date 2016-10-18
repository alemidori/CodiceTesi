from gensim import corpora, models
import create_nyt_dataset

def calculate_topic_distribution():
    terms = {}
    corpus, dictionary = create_dictionary()
    Lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=300)

    for k in Lda_model.show_topics(num_topics=300,num_words=50,formatted=False):
        termslist = []
        for i in range(0, 50):
            termslist.append(k[1][i][0])
        terms[k[0]] = termslist


    corpus_Lda = Lda_model[corpus]
    corpora.BleiCorpus.serialize('tmp/corpus_nyt.lda-c', corpus_Lda)
    calculate_main_topic(corpus_Lda, terms)
    return

def create_dictionary():
    toks = get_tokens()
    print("JBKBKBHVJHB "+str(len(toks)))
    dictionary = corpora.Dictionary(toks)
    corpus = [dictionary.doc2bow(token) for token in toks]
    print("Dizionario creato.")
    return corpus, dictionary

def update_result_keywords_collection(num_topic, list_LDAkeywords):
    cursor = create_nyt_dataset.result_keywords.find()
    count = cursor.count()
    print(str(count))
    print("num_topic "+str(len(num_topic)))
    print("listLDA "+str(len(list_LDAkeywords)))
    increment = 0
    for el in cursor:
        if increment == count:
            print("out of rangeee")
            break
        elif increment < count:
            print(increment)
            el['topic'] = num_topic[increment]
            el['LDA_keywords'] = list_LDAkeywords[increment]
            create_nyt_dataset.result_keywords.save(el)
            increment += 1

    return


def calculate_main_topic(ldamodel, terms):

    max_list = []
    for doc in ldamodel:
        single_list = []  # singola lista di topic per ciascun paragrafo
        max_dict = {}
        for n in doc:  # per ogni topic nel pragrafo
            single_list.append(n[1])  # appendo il valore della sua distribuzione
        for n in doc:
            if n[1] == max(single_list) and n[1] not in max_dict.values():  # trovo il topic con maggiore distribuzione
                max_dict[n[0]] = n[1]
        max_list.append(max_dict)


    list_topicmax = []
    print("maxlist!! "+str(len(max_list)))
    print(max_list)
    for elem in max_list:
        for key in elem.keys():
            list_topicmax.append(key)
    #list_topicmax = sum(list_topicmax, [])
    print(list_topicmax)
    print("topicmax!! "+str(len(list_topicmax)))

    termstopics = []
    for i in range(0, len(list_topicmax)):
        termstopics.append(terms[list_topicmax[i]])

    update_result_keywords_collection(list_topicmax, termstopics)

    return list_topicmax

def get_tokens():
    token_list = []
    cursor = create_nyt_dataset.result_keywords.find()
    count = cursor.count()
    print("COUNT "+str(count))
    for element in cursor:
        token_list.append(element['tokens'])  #e' una lista di liste in cui ogni lista interna ha i token
        # riferiti ad ogni singolo paragrafo
    #print("sdbhjsd "+str(len(token_list)))
    return token_list

#create_nyt_dataset.create_filtered_nyt()
create_nyt_dataset.save_frequency_allcorpus()
#calculate_topic_distribution()
