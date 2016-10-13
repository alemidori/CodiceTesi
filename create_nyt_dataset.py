import pymongo
from string import punctuation
from itertools import chain
from collections import Counter
import datetime
import processing

client = pymongo.MongoClient()
db_nyt = client['nyt_dataset']

tokens_coll = db_nyt['tokens']
tokens_filtered = db_nyt['filtered_tokens']

def filter_date():
    list_dict = []
    normalized_tokens = []
    tokens = []

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
        #print(tokens_norm)
        #print(tokens)
        keywords_listdict = el['keywords']
        for k in keywords_listdict:
            keywords.append([k for k in ''.join(c for c in k['value'] if c not in punctuation).lower().split()])

        flat = sum(keywords, [])
        flat_nostopwords = processing.remove_stopwords(flat)
        #print(flat_nostopwords)
        elemdict['text'] = el['text']
        elemdict['tokens'] = tokens_norm
        elemdict['keywords'] = flat_nostopwords

        list_dict.append(elemdict)

    for item in list_dict[:10]:
        print(item)
    return

filter_date()