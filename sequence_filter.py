# DeMMO TCS pipeline -- sequence_filter.py 
# Goal of this script: for each TSV file containing all sequence names with associated IPR signatures, 
# pull out the HK protein names and relevant IPR signatures. For each TSV input with a genome file name, 
# this will create a CSV output with the same genome file name. 
# Run this script AFTER running .faa files through InterProScan and BEFORE running scripts to pull out 
# HK sequences from .faa files. Can be run in tandem with IPR_filter.py. 

# Import relevant environments 
import csv
import collections
import os
import re
import sys
from os import path
import glob

# Set directory paths, including the base directory, the directory where the .tsv InterProScan outputs 
# can be found, and the directory where you would like to put the .csv HK sequence list outputs.
basedir = "/home/"
TSVpath = os.path.join(basedir, "IPR/")
seqpath = os.path.join(basedir, "indv_HKseq_names/")

# Set paths for locations of HK true and false lists. If desired, can also run this script to pull out RR
# sequence names, so RR true and false lists are also included but commented out for now.
HKtrue_list = os.path.join(basedir, "DeMMOworkflow/HK1ListTSV.txt")
HKfalse_list = os.path.join(basedir, "DeMMOworkflow/HKFalseListTSV.txt")
#RRtrue_list = os.path.join(basedir, "DeMMOworkflow/RR1ListTSV.txt")
#RRfalse_list = os.path.join(basedir, "DeMMOworkflow/RRFalseListShortTSV.txt")

# Define functions to identify HK IPR signatures 

def IPR_results(file):
    #Create dictionary from InterProScan results with ORFs (protein sequence names from .faa file)
    # as keys and IPR signatures list for each protein as values
    with open(file, "rt") as tsvFile:
        IPRReader= csv.reader(tsvFile, delimiter="\t")
        workingProtDict = collections.defaultdict(list)
        # Identify the two columns of interest from the .tsv IPR output file 
        for line in IPRReader:
            if len(line)>=12:
                protID=line[0]
                interpro=line[11]
                if interpro != '':
                    workingProtDict[protID].append(interpro)
                    continue
            else:
                continue
    return workingProtDict

def IPR_list(file):
    #Import list of IPR signatures for HKs (both positve and negative hits) -- these are the lists that were 
    # imported above (this function also works to import list of RR signatures if desired)
    with open(file, "rt") as tsvFile:
        temp = csv.reader(tsvFile, delimiter="\t")
        IPRlist = []
        #Turn IPR signatures in file into a list
        for line in temp:
            IPRlist.append(line)
            #Flatten nested sublists
        IPRlist = [val for sublist in IPRlist for val in sublist]
    return IPRlist

def IPR_filter(IPRdict, pos_list, neg_list): 
    # Filter ORFs for IPRs matching true (but not false) IPR signatures. This is so we can pull out relevant 
    # HKs that have ATPase domains identified with IPR signatures, but not false positives that are actually 
    # other proteins. 
    posdict = {}
    filtdict = {}
    pos_set = set(pos_list)
    neg_set = set(neg_list)
    # Create dictionary (posdict) containing only ORFs with at least one true associated IPR signature 
    for key, val in IPRdict.items():
        val_set = set(val)
        if len(val_set.intersection(pos_set)) > 0:
            posdict[key] = val
    # Create dictionary containing only ORFs with at least one true IPR signature but not one of the false IPR signatures
    for key, val in posdict.items():
        val_set = set(val)
        if len(val_set.intersection(neg_set)) == 0:
            filtdict[key] = val
    return filtdict

def main():
    # Create a dictionary of IPR signatures for each .tsv file found in the TSVpath directory, then filter out HK 
    # true positives and create a new file in the seqpath directory with the same file name as the .tsv file (the 
    # genome name). For every .tsv file input with all identifed proteins in a genome, there is a .csv output with 
    # just HKs and associated IPR signatures. This can be used with RRs too -- the RR relevant portions are currently 
    # commented out. 

    # Change directory to TSVpath
    os.chdir(TSVpath)
    for file in glob.glob("*.tsv"):
        # Make a new file with the same name, but located in seqpath directory as .csv 
        with open(os.path.join(seqpath, (file.rsplit(".",1)[0]) + ".csv"), "w") as outfile: 
            wr = csv.writer(outfile)

            # Create dictionary of all ORFs and associated IPRs, list of true HKs and false HKs signatures
            IPRdict = IPR_results(file)
            HKpos = IPR_list(HKtrue_list)
            HKneg = IPR_list(HKfalse_list)
            #RRpos = IPR_list(RRtrue_list)
            #RRneg = IPR_list(RRfalse_list)
        
            HKfilt = IPR_filter(IPRdict, HKpos, HKneg)
            print("The number of HKs is",len(HKfilt))
            #RRfilt = IPR_filter(IPRdict, RRpos, RRneg)
            #print("The number of RRs is", len(RRfilt))
        
            for key, val in HKfilt.items():
                wr.writerow([key, val])
            #for key, val in RRfilt.items():
                #wr.writerow([key, val])

# Run the whole script 
if __name__ == "__main__":
    main()
