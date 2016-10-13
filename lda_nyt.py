from gensim import corpora, models
import create_nyt_dataset

def calculate_topic_distribution():
    terms = {}

    corpus,dictionary = create_dictionary()
    Lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=300)

    for k in Lda_model.show_topics(num_topics=300,num_words=50,formatted=False):
        termslist = []
        for i in range(0,50):
            termslist.append(k[1][i][0])
        terms[k[0]] = termslist

    corpus_Lda = Lda_model[corpus]
    corpora.BleiCorpus.serialize('tmp/corpus_nyt.lda-c', corpus_Lda)
    calculate_main_topic(corpus_Lda, terms)
    return

def create_dictionary():
    stemmed = create_nyt_dataset.get_tokens()
    dictionary = corpora.Dictionary(stemmed)
    corpus = [dictionary.doc2bow(token) for token in stemmed]
    print("Dizionario creato.")
    return corpus, dictionary

def update_result_keywords_collection(num_topic, list_LDAkeywords):
    cursor = create_nyt_dataset.result_keywords.find()
    count = create_nyt_dataset.result_keywords.count()
    print("num_topic "+str(len(num_topic)))
    print("listLDA "+str(len(list_LDAkeywords)))
    print(str(count))
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

    for elem in max_list:
        for key in elem:
            list_topicmax.append(key)

    termstopics = []
    for i in range(0, len(list_topicmax)):
        termstopics.append(terms[list_topicmax[i]])

    update_result_keywords_collection(list_topicmax, termstopics)

    return list_topicmax

calculate_topic_distribution()