import lda_nyt
import hdp_nyt
import merge_keywords
import manage_nyt_dataset
import auto_composition
import methods_composition
import configurations_performarce

import lcs
import relations
import graph_relations

#manage_nyt_dataset.create_filtered_nyt() #creo il dataset filtrando alcuni record dall'originale
#manage_nyt_dataset.save_frequency_allcorpus() #salvo le frequenze dei termini in una collection
#hdp_nyt.calculate_topic_distribution()
#merge_keywords.merge_keywords_and_specificwords_from_documents()
#merge_keywords.remove_empty()
#lda_nyt.calculate_topic_distribution() #calcolo i topic tramite lda
#manage_nyt_dataset.add_specific_words_to_collection() #inserisco i termini specifici nella collect.
#auto_composition.compose_methods() #configurazioni e salvataggio risultati
#methods_composition.compose_methods()
#configurations_performarce.process_performance()


#___________________________prove metodi singoli
terms = []
specific = []
for item in manage_nyt_dataset.topicsecription.find({'topic': 30}):

    for tuple in item['tuple_terms']:
        terms.append(tuple[0])
    for term in item['specific_words_in_documents']:
        specific.append(term)

print(terms)
print(specific)
input_tuples = []
input_spec = []
for t in terms:
    input_tuples.append((t, 0))
for t in specific:
    input_spec.append((t, 0))

tuples = graph_relations.process(input_spec)
for t in tuples:
    print(t[0])

#____________________________



#print('Processo terminato.')