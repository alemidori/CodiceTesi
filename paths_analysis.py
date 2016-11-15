import csv
import numpy as np
import glob
import os


def parse_files():
    files = glob.glob('tsvs/*.tsv')
    for file in files:
        filename = os.path.basename('tsvs/'+file)
        with open(file, 'r') as f:
            jumps_list = []
            none_jumps = []
            toomany_jumps = []
            tsvreader = csv.reader(f, delimiter="\t")
            for line in tsvreader:
                if line[3] != '-1' and line[3] != 'None':
                    jumps_list.append(line[3])
                if line[3] == 'None':
                    none_jumps.append(line[3])
                if line[3] == '-1':
                    toomany_jumps.append(line[3])

            mean_jumps_list = np.mean(jumps_list)

            with open('paths_analysis.tsv', 'a') as analysis_file:
                analysis_file.write(
                    str(filename) + '\t' + str(len(jumps_list)) + '\t' + str(mean_jumps_list) + '\t' + str(
                        len(none_jumps)) + '\t' + str(len(toomany_jumps)))
                analysis_file.write('\n\n')
                analysis_file.close()
        f.close()
    return

parse_files()
