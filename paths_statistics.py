import csv
import numpy as np
import glob
import os

def parse():
    files = glob.glob('tsvs/*.tsv')
    for file in files:
        filename = os.path.basename(file)
        print (filename)
        with open (file,'r') as f:
            jumps_list = []
            none_jumps = []
            toomany_jumps = []
            row_count = 0
            tsvreader = csv.reader(f, delimiter="\t")
            for line in tsvreader:
                row_count +=1
                if (len(line) > 1):
                    print('riga: ')
                    print(line[0], line[1], line[2], line[3], line[4])
                    print(line[4])
                    if line[4] != '-1' and line[4] != 'None':
                        jumps_list.append(int(line[4]))
                    if line[4] == 'None':
                        none_jumps.append(line[4])
                    if line[4] == '-1':
                        toomany_jumps.append(line[4])

            print(jumps_list, none_jumps, toomany_jumps)

            mean_jumps_list = np.mean(jumps_list)
            percjump = 100 * float(len(jumps_list)) / float(row_count-2)
            percnonejump = 100 * float(len(none_jumps)) / float(row_count-2)
            perctoomanyjumps = 100 * float(len(toomany_jumps)) / float(row_count-2)
            with open('paths_statistics.tsv', 'a') as statistics_file:
                statistics_file.write(
                    str(filename) + '\t' + str(percjump) + '\t' + str(mean_jumps_list) + '\t' + str(
                        percnonejump) + '\t' + str(perctoomanyjumps))
                statistics_file.write('\n')
                statistics_file.close()
        f.close()

parse()
