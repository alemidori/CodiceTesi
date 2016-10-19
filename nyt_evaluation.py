import lda_nyt
import create_nyt_dataset
import auto_composition

create_nyt_dataset.create_filtered_nyt() #creo il dataset filtrando alcuni record dall'originale
lda_nyt.calculate_topic_distribution() #calcolo i topic tramite lda
create_nyt_dataset.save_frequency_allcorpus() #salvo le frequenze dei termini in una collection
create_nyt_dataset.add_specific_words_to_collection() #inserisco i termini specifici nella collect.
#auto_composition.compose_methods() #configurazioni e salvataggio risultati

print('Processo terminato.')