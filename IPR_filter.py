# This script takes outputs of proteins identified in InterProScan and filters out proteins of interest. 
# List of proteins of interest can be changed with the true and false HK and RR lists. 
# Can be generalized to just be true and false lists for any proteins, not specifically only HKs and RRs. 

# Be sure you have defined paths for all your input and output files

import csv
import collections
import os

# Define base directory, which should contain the
basedir = "path/to/base/directory"

# Define path for .tsv outputs from Interproscan. Change depending on where your .tsv outputs are stored.
TSVpath = "path/to/tsv"

# Define path for where you want the .csv outputs containing HK and RR counts to be stored
CSVpath = "/Users/emilyfulk/DeMMOworkflow/test_data"

# Define path to first file in TSVpath (this is just the first file in the working directory - given as an example here, although your file name will be different),
IPRresults = os.path.join(TSVpath,"FAA_ID2773858020.SLURM_JOB_ID2470156.tsv")

# Define path to HK and RR true and false positive lists
HKtrue_list = os.path.join(basedir, "HK_RR_IPRsignatures/HK1ListTSV.txt")
HKfalse_list = os.path.join(basedir, "HK_RR_IPRsignatures/HKFalseListTSV.txt")
RRtrue_list = os.path.join(basedir, "HK_RR_IPRsignatures/RR1ListTSV.txt")
RRfalse_list = os.path.join(basedir, "HK_RR_IPRsignatures/RRFalseListShortTSV.txt")

for p in [TSVpath, CSVpath, IPRresults]:
  if not os.path.exists(p):
    print("Path does not exist", p)
    exit()

def IPR_results(file):
  #Create dictionary from InterProScan results with ORFs as keys and IPR list as values
  with open(os.path.join(TSVpath, file), "rt") as tsvFile:
    IPRReader= csv.reader(tsvFile, delimiter="\t")
    workingProtDict = collections.defaultdict(list)
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
  #Imports list of IPRs for HKs (both positve and negative hits) and RRs
  with open(file, "rt") as tsvFile:
    temp = csv.reader(tsvFile, delimiter="\t")
    IPRlist = []
    #Turn IPR signatures in file into a list
    for line in temp:
      IPRlist.append(line)
    #Flatten nested sublists
    IPRlist = [val for sublist in IPRlist for val in sublist]
  return IPRlist

def IPR_filter(IPRdict, pos_list, neg_list): # Filters ORFS for IPRs matching true (but not false) IPR signatures
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

def filewriter(filtdict, fileout): # Writes .csv file containing each ORF associated with the desired IPR set
  cats=filtdict.keys()
  with open(fileout, "w") as outfile:
    wr = csv.writer(outfile)
    headers=["Genome", "ORFs and IPRs"]
    wr.writerow(headers)
    for cat in cats:
      data = [cat, filtdict[cat][0]]
      wr.writerow(data)

def masterfilewriter(masterDictionary, fileout): # Writes .csv file containing a summary of all the HKs and RRs filtered from a directory
  cats = masterDictionary.keys()
  with open(fileout, "w") as outfile:
    wr = csv.writer(outfile)
    headers=["Genome","# HKs","# RRs"]
    wr.writerow(headers)
    for cat in cats:
      data = [cat, masterDictionary[cat][0], masterDictionary[cat][1]]
      wr.writerow(data)

def main(): # sets positive and negative lists and input based on the input files above 
  # prints 3 files: all HKs in directory (ORFs and IPRs), all RRs in directory 
  # (ORFs and IPRs), and summary file of each genome in directory, #HKs, #RRs
  
  IPRdict = IPR_results(IPRresults)
  HKpos = IPR_list(HKtrue_list)
  HKneg = IPR_list(HKfalse_list)
  RRpos = IPR_list(RRtrue_list)
  RRneg = IPR_list(RRfalse_list)
  
  # write results for HKs
  filtdict = {}
  # change directory path
  for filename in os.listdir(TSVpath):
    if filename.endswith(".tsv"):
      IPRdict = IPR_results(filename)
      HKfilt = IPR_filter(IPRdict, HKpos, HKneg)
      filtdict[(filename)] = [HKfilt]

    filewriter(filtdict, os.path.join(CSVpath, "HK_IPR_signatures.csv"))

  # write results for RRs
  filtdict = {}
  # change directory path
  for filename in os.listdir(TSVpath):
    if filename.endswith(".tsv"):
      IPRdict = IPR_results(filename)
      RRfilt = IPR_filter(IPRdict, RRpos, RRneg)
      filtdict[(filename)] = [RRfilt]

    filewriter(filtdict, os.path.join(CSVpath, "RR_IPR_signatures.csv"))
    
  # write summary file with genome ID, #HKs, and #RRs
  masterDictionary = {}
  # change directory path 
  for filename in os.listdir(TSVpath):
    if filename.endswith(".tsv"):
      IPRdict = IPR_results(filename)
      HKfilt = IPR_filter(IPRdict, HKpos, HKneg)
      RRfilt = IPR_filter(IPRdict, RRpos, RRneg)
      masterDictionary[str(filename)] = [len(HKfilt), len(RRfilt)]

    # change summary output file name
    masterfilewriter(masterDictionary, os.path.join(CSVpath,"HK_RR_abundance_counts.csv"))

if __name__ == "__main__":
  main()
