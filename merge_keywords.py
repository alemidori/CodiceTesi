import manage_nyt_dataset
import specificity_nyt
from collections import Counter

cursor = manage_nyt_dataset.topicsecription.find()
cursor_doc_distr = manage_nyt_dataset.document_distribution.find()

def merge_keywords_and_specificwords_from_documents():
    #prendi i primi 10 documenti (se non ce ne sono 10 prendi tutti quelli che ci sono) in ogni topic

    for item in cursor_doc_distr:
        specific_merged = []
        keywords_merged = []
        print("**********Cambio topic")
        topicterms = []
        topic = item['topic']
        docdistributionlist = item['document_distribution']
        doclist = []
        if len(docdistributionlist) >= 5:
            for i in range(0, 5):
                doclist.append(docdistributionlist[i][0])

        doc_details = []
        for k in doclist:
            cursor_pos = manage_nyt_dataset.result_keywords.find({'position': k})
            for element in cursor_pos:
                doc_details.append(element)

        cursor_topic_distr = manage_nyt_dataset.topicsecription.find({'topic': topic})
        for el in cursor_topic_distr:
            for n in el['tuple_terms']:
                topicterms.append(n[0])

        for doc in doc_details:
            # print('Aggiungo termini dal documento...')
            keywords = doc['text_keywords']
            tokens = doc['tokens']
            print('topicterms'+str(topicterms))
            print('doctokens'+str(tokens))
            specific = specificity_nyt.get_specific_words(topicterms, tokens)
            print(specific)
            specific_merged.append(specific)
            keywords_merged.append(keywords)
        cursor_topic_distr.close()
        cursor_topic_distr = manage_nyt_dataset.topicsecription.find({'topic': topic})
        for element in cursor_topic_distr:
            keywords_tuples = []
            counter = dict(Counter(sum(keywords_merged, [])))
            for k, v in counter.items():
                keywords_tuples.append((k, v))
            element['merged_keywords_in_documents'] = keywords_tuples
            element['specific_words_in_documents'] = list(set(sum(specific_merged, [])))
            manage_nyt_dataset.topicsecription.save(element)

    return

def remove_empty():
    print('Rimozione record con campo merged_keywords vuoto...')
    manage_nyt_dataset.topicsecription.remove({'merged_keywords_in_documents': []})

    return