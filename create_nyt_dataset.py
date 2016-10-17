import pymongo
from string import punctuation
import datetime
import processing

client = pymongo.MongoClient()
db_nyt = client['nyt_dataset']

tokens_coll = db_nyt['tokens']
result_keywords = db_nyt['results']

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

