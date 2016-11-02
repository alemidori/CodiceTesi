from gensim import corpora, models
import manage_nyt_dataset

def calculate_topic_distribution():
    terms = {}
    corpus, dictionary = create_dictionary()
    Lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=300)

    for k in Lda_model.show_topics(num_topics=300,num_words=20,formatted=False):
        termslist = []
        for i in range(0, 20):
            termslist.append(k[1][i][0])
        terms[k[0]] = termslist

    corpus_Lda = Lda_model[corpus]
    corpora.BleiCorpus.serialize('tmp/corpus_nyt.lda-c', corpus_Lda)
    notopic_documents = check_notopic_documents(corpus_Lda)
    if notopic_documents:
        remove_notopic_documents(notopic_documents)
    else:
        calculate_main_topic(corpus_Lda, terms)
    return

def create_dictionary():
    toks = get_tokens()
    dictionary = corpora.Dictionary(toks)
    corpus = [dictionary.doc2bow(token) for token in toks]
    print("Dizionario creato.")
    return corpus, dictionary

def update_result_keywords_collection(num_topic, list_LDAkeywords):
    cursor = manage_nyt_dataset.result_keywords.find()
    count = cursor.count()
    print("num_topic "+str(len(num_topic)))
    print("listLDA "+str(len(list_LDAkeywords)))
    increment = 0
    for el in cursor:
        if increment < count:
            el['topic'] = num_topic[increment]
            el['LDA_keywords'] = list_LDAkeywords[increment]
            manage_nyt_dataset.result_keywords.save(el)
            increment += 1
        else:
            break
    return


def calculate_main_topic(ldamodel, terms):
    print('Calcolo i topic dominanti in ciascun documento...')
    list_topicmax = []
    for doc in ldamodel:
        flag = 0
        for n in doc:
            if n[1] == max([n[1] for n in doc]) and flag == 0:
                list_topicmax.append(n[0])
                flag = 1
    print("Lista topic dominanti: "+str(len(list_topicmax)))
    termstopics = []
    for item in list_topicmax:
        termstopics.append(terms[item])
    update_result_keywords_collection(list_topicmax, termstopics)
    return list_topicmax

def check_notopic_documents(ldamodel):
    print('Verifica dei topic in ciascun documento...')
    inc = 0
    notopic_documents = []
    for doc in ldamodel:
        if not doc:
            print('Non ci sono topic nel doc: '+str(inc))
            notopic_documents.append(inc)
        inc += 1
    return notopic_documents

def remove_notopic_documents(notopicdoc):
    for number in notopicdoc:
        print('Rimuovo record con position: '+str(number))
        manage_nyt_dataset.result_keywords.remove({'position': number})

    print('Dopo rimozione: ' + str(manage_nyt_dataset.result_keywords.count()))
    calculate_topic_distribution() #rieseguo lda sui documenti con topic
    return

def get_tokens():
    token_list = []
    cursor = manage_nyt_dataset.result_keywords.find()
    for element in cursor:
        token_list.append(element['tokens'])  #e' una lista di liste in cui ogni lista interna ha i token
        # riferiti ad ogni singolo paragrafo
    #print("sdbhjsd "+str(len(token_list)))
    return token_list


