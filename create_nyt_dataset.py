import pymongo
from string import punctuation
import datetime
import processing
from itertools import chain
from collections import Counter

client = pymongo.MongoClient()
db_nyt = client['nyt_dataset']

tokens_coll = db_nyt['tokens']
result_keywords = db_nyt['results']
term_frequency = db_nyt['term_frequency']

list_dict = []

def filter_date():

    cursor = tokens_coll.find({'$and':
                                   [{'keywords': {'$gt': []}},
                                    {'pub_date': {'$gte': datetime.datetime(1960, 1, 1)}}
                            ]})
    print(cursor.count())
    for el in cursor:
        keywords = []
        elemdict = {}
        tokens = el['tokens']
        tokens_norm = [t.lower() for t in tokens]
        keywords_listdict = el['keywords']
        for k in keywords_listdict:
            keywords.append([k for k in ''.join(c for c in k['value'] if c not in punctuation).lower().split()])

        flat = sum(keywords, [])
        flat_nostopwords = processing.remove_stopwords(flat)
        elemdict['text'] = el['text']
        elemdict['tokens'] = tokens_norm
        elemdict['keywords'] = flat_nostopwords

        list_dict.append(elemdict)

    return

def create_filtered_nyt():
    filter_date()
    for item in list_dict:
        result_keywords.insert_one({'text': item['text'], 'tokens': item['tokens'] , 'text_keywords': item['keywords']})
    return

def insert_terms_frequency(term, freq):
    term_frequency.insert_one({'term': term, 'frequency': freq})
    return

def save_frequency_allcorpus():
    alltokens = []
    print("Sto raccogliendo tutti i token...")
    # salvo una lista con tutte le liste di token di tutti i documenti del corpus in modo da poter calcolare la specificità
    for p in result_keywords.find(None, {'_id': 0, 'tokens': 1}):
        alltokens.append(p['tokens'])

    print("Ho finito di raccogliere i token.")

    print("Conto le occorenze nella lista di token del corpus...")
    # riduco la lista di liste ad una singola lista con tutto mergiato per poter contare le occorrenze dei termini
    all_list = chain.from_iterable(alltokens)
    term_freqs_all = Counter(all_list)

    print("Riduzione ad un'unica lista terminata.")

    for x in term_freqs_all.keys():
        insert_terms_frequency(x, term_freqs_all[x])
    return