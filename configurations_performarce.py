import manage_nyt_dataset
import itertools

def process_performance():
    manage_nyt_dataset.performance_config.remove({}) #se esiste la collection la rimuove
    cursor = manage_nyt_dataset.topicsecription.find()
    methodslist = ['lcs', 'relations', 'graph_relations']
    print('Calcolo permutazioni...')
    test = itertools.permutations(methodslist)
    configlist = list(test)

    stringconfig = []
    all_config = []
    print('Produzione stringhe configurazioni...')
    for config in configlist:
        stringconfig.append(str(config[0] + '-' + config[1] + '-' + config[2]))
    for string in stringconfig:
        all_config.append(string)
        all_config.append(str('SPECIFICITY-'+string))
    try:
        for item in cursor:
            topic = item['topic']

            print('--- Topic ' + str(topic) + ' ---')
            hdp_terms = []
            for k in item['tuple_terms']:
                hdp_terms.append(k[0])
            keywords = item['merged_keywords_in_documents']
            paramlists = []
            hdp_precision, hdp_recall, hdp_Fmeasure = calculate_precision_recall(hdp_terms, keywords)
            print('HDPPrecision: ' + str(hdp_precision) + ' HDPRecall: ' + str(hdp_recall) + ' HDPFmeasure: '
                  + str(hdp_Fmeasure))
            for conf in all_config:
                result = []
                for k in item[conf]:
                    result.append(k[0])
                precision, recall, Fmeasure = calculate_precision_recall(result, keywords)
                print('Precision: ' + str(precision) + ' Recall: ' + str(recall) + ' Fmeasure: ' + str(Fmeasure))
                paramlists.append([conf, precision, recall, Fmeasure])
            paramlists.append(['HDP', hdp_precision, hdp_recall, hdp_Fmeasure])
            save_in_collection(topic, paramlists)
    except KeyError:
        print('Topic non processati... Configurazioni inesistenti.')
    return

def calculate_precision_recall(result_config, keywords):
    relevant_retrieved = 0
    for element in result_config:
        if element in keywords:
            relevant_retrieved += 1

    precision = relevant_retrieved/len(result_config)
    recall = relevant_retrieved/len(keywords)
    try:
        Fmeasure = 2*((precision*recall)/precision+recall)
    except ZeroDivisionError:
        Fmeasure = 0

    return precision, recall, Fmeasure

def save_in_collection(topic, paramlists):
    jsonToExport = {}
    jsonToExport.update({'topic':topic})
    for element in paramlists:
        json = {element[0] : {'precision' : element[1] , 'recall' : element[2] , 'Fmeasure' : element[3]}}
        jsonToExport.update(json)

    manage_nyt_dataset.performance_config.insert_one(jsonToExport)

    return