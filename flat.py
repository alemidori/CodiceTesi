import manage_nyt_dataset

cursor = manage_nyt_dataset.topicsecription.find().limit(1)
for record in cursor:
    record['SPECIFICITY-relations-lcs-graph_relations'] = [['psychological_feature', 0.0], ['concept', 0.0], ['person', 0.0]]
    manage_nyt_dataset.topicsecription.save(record)
