import manage_nyt_dataset
import cmath
from collections import Counter


def get_specific_words(Ldawords, tokenlist):
    specific_words = []
    term_freqs = Counter(tokenlist)
    total_f = list(manage_nyt_dataset.term_frequency.aggregate([{'$group': {'_id': None, 'count': {'$sum': 1}}}]))[0]['count']


    for word in Ldawords:
        tf = 0
        tf_all = 1

        if word in term_freqs.keys():
            for t in term_freqs.keys():
                if t == word:
                    tf = float(term_freqs[t]) / len(tokenlist)

            for k in manage_nyt_dataset.term_frequency.find({'term': word}, {'_id':0, 'frequency':1}):
                tf_all = float(k['frequency']) / total_f
            try:
                specificity = (tf - tf_all)/cmath.sqrt(tf_all)

            except KeyError:
                specificity = -1

            if cmath.phase(specificity) > -0.5:
                specific_words.append(word)

    return specific_words
