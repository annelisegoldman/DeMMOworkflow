# This script concatenates all HK-associated IPRs from all sites
# As inputs, it takes .csv files from each genome that lists the name of each HK sequence and the IPRs associate with it

import csv
import re
from pathlib import Path
import ast
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

basedir = Path("/Users/emilyfulk/Desktop/allIPRtest")
inbox = basedir / "inbox"

def concat_iprs_dict(file): #Creates nested dictionary of {'faa_id':{'sequence name'}:{['IPR#...']}} for each file

    # extract MAG ID from file name
    faa_id_pattern = re.compile('[0-9]+')
    faa_id = int(re.search(faa_id_pattern, file.name).group(0))

    # extract {'sequence name':['IPR#...']} from csv file
    with open(file, "rt") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        file_dict = {row[0]: ast.literal_eval(row[1]) for row in reader}

    return file_dict, faa_id

def parse_dict(global_dict):
    # initiate global list of all IPR signatures
    global_lst = []

    # remove '-' and duplicate entries from list of IPRs. Note: for each sequence, an IPR will only be counted once.
    for outer_key, inner_key in global_dict.items():
        for key, value in inner_key.items():
            tidy_lst = [i for i in value if '-' not in i]
            tidy_lst.append('test')
            inner_key[key] = list(set(tidy_lst))

            for i in tidy_lst:
                if i not in global_lst:
                    global_lst.append(i)

    return global_dict, global_lst

def calc_frequencies(global_dict, global_lst, seq_count_dict):

    # create dataframe for storing IPR frequency by site and IPR
    sites = [1,2,3,4,5,6,7,8]

    mindex = pd.MultiIndex.from_product([sites,global_lst], names = ['Site','IPR'])

    freq_data = pd.DataFrame(index = mindex, columns = ['Total count','Frequency per sequence (%)'])

    # count the number of times each IPR occurs at each site
    for s in sites:
        # create a dictionary for {site : # of protein sequences}
        site_dict = {outer_key:inner_key for outer_key,inner_key in global_dict.items() if int(str(outer_key)[0]) == s}

        site_seq_count_dict = {key: value for key, value in seq_count_dict.items() if int(str(key)[0]) == s}

        site_seq_count = sum(site_seq_count_dict.values())

        # iterate through global list and count whether IPR is in list
        for i in global_lst:
            ipr_count =0
            for outer_key,inner_key in site_dict.items():
                for inner_key, value in inner_key.items():
                    if i in value:
                        ipr_count +=1

            freq_data['Total count'].at[s,i] = ipr_count

        if site_seq_count > 0:
            freq_data['Frequency per sequence (%)'] = (freq_data['Total count'] / site_seq_count)*100

    return freq_data

def main():

    raw_dict = {}
    seq_count_dict = {}

    # iterate through .csv files to count # of sequences and collected IPR lists into raw_dict {sequence name: ['IPR##'..]}
    for file in inbox.glob('*.csv'):
        file_dict, faa_id = concat_iprs_dict(file)
        raw_dict[faa_id] = file_dict
        seq_count = len(file_dict.keys())
        seq_count_dict[faa_id]= seq_count

    # tidy dictionary and compile list of IPRs
    global_dict, global_lst = parse_dict(raw_dict)

    # calculate frequence of each IPR as a % of sequences per site
    freq_df = calc_frequencies(global_dict, global_lst, seq_count_dict)

    # parse data for plotting
    percent_df = freq_df['Frequency per sequence (%)'].unstack().fillna(0)

    # plot heatmap
    fig = sns.heatmap(percent_df, vmin = 0, vmax = 100, cmap = 'viridis', annot = True)
    fig.set_title('Frequency per site (%)')
    plt.show()

if __name__ == "__main__":
    main()