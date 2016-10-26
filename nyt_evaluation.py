import lda_nyt
import hdp_nyt
import merge_keywords
import create_nyt_dataset
import auto_composition
import methods_composition

#create_nyt_dataset.create_filtered_nyt() #creo il dataset filtrando alcuni record dall'originale
#create_nyt_dataset.save_frequency_allcorpus() #salvo le frequenze dei termini in una collection
hdp_nyt.calculate_topic_distribution()
merge_keywords.merge_keywords_and_specificwords_from_documents()
merge_keywords.remove_empty()
#lda_nyt.calculate_topic_distribution() #calcolo i topic tramite lda
#create_nyt_dataset.add_specific_words_to_collection() #inserisco i termini specifici nella collect.
#auto_composition.compose_methods() #configurazioni e salvataggio risultati
methods_composition.compose_methods()

print('Processo terminato.')