import csv
import glob

abstracts = []
keywords = []
files = glob.glob('../Scopus/*.csv')
for file in files:

    with open(file, 'r') as f:
        rows = []
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

        abstracts.append(rows[1][rows[0].index('Abstract')])
        keywords.append(rows[1][rows[0].index('Author Keywords')].split('; '))


print(abstracts)
print(keywords)
