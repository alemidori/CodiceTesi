from gensim import corpora, models
import manage_nyt_dataset

def create_dictionary():
    toks = get_tokens()
    dictionary = corpora.Dictionary(toks)
    corpus = [dictionary.doc2bow(token) for token in toks]
    print("Dizionario creato.")
    dictionary.save('tmp/dictionary.dict')
    return corpus, dictionary

def calculate_topic_distribution():
    manage_nyt_dataset.topicsecription.remove({})
    #dictionary = corpora.Dictionary.load('tmp/dictionary.dict')
    #corp = corpora.BleiCorpus('tmp/corpus_nyt.hdp-c')
    corpus, dictionary = create_dictionary()
    hdpmodel = models.HdpModel(corpus, id2word=dictionary)

    hdpmodel_corp = hdpmodel[corpus]
    create_topic_document_distribution(hdpmodel_corp)

    for k in hdpmodel.show_topics(topn=10, topics=-1, formatted=False):
        manage_nyt_dataset.topicsecription.insert_one({'topic': k[0], 'tuple_terms': k[1]})
    return

def get_tokens():
    token_list = []
    cursor = manage_nyt_dataset.result_keywords.find()
    for element in cursor:
        token_list.append(element['tokens'])
    return token_list


def create_topic_document_distribution(corpus):
    manage_nyt_dataset.document_distribution.remove({})
    print ("Creazione collezione delle distribuzioni dei documenti, divisi per topic.")
    topic_document_distribution = {}
    i = 0
    for element in corpus:
        print ("Collezione distribuzioni documenti, divisi per topic; Iteration: " + str(i))
        # recupero l'ID del document associato all'indice
        document_id = i
        # incremento il contatore per il prossimo ID
        i += 1
        # scorro la lista delle distribuzioni dei topic del documento e aggiungo ogni topic al dizionario
        for tuples in element:
            try:
                topic_document_distribution[tuples[0]].append((document_id,tuples[1]))
            except KeyError:
                topic_document_distribution[tuples[0]] = [(document_id, tuples[1])]

    for k, v in topic_document_distribution.items():
        sortedv = sorted(v, key=lambda x: x[1], reverse=True)
        json_to_insert = {'topic': k, 'document_distribution': sortedv}
        manage_nyt_dataset.document_distribution.insert_one(json_to_insert)
    print ("Creazione collezione completata.")
    print ("Creazione indici.")
    manage_nyt_dataset.document_distribution.create_index([("document_distribution.document_id", manage_nyt_dataset.ASCENDING)])
    print ("Creazione indici completata.")
    return