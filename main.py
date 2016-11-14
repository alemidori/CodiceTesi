import splitting
import terms_dictionary
import logging
import storage
import main_topic_distribution
import main_topic_specification
import glob

#serve per stampare anche i log durante la fase di esecuzione
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


#path = "../gtexts/*.txt"
#files = glob.glob(path)  # lista di file txt da spezzare in paragrafi
#file = "../gtexts/_CHH9KN1bO5cs_GHjQ-r1A.txt"

def main(files):

    splitting.process_texts(files)

    terms_dictionary.create_terms_dictonary()

    storage.save_frequency_allcorpus()

    main_topic_distribution.main()

    main_topic_specification.main()
    return


#main(files)
#print("Collezioni create. Processo terminato.")