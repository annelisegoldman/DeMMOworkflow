# This script takes outputs of proteins identified in InterProScan and filters out proteins of interest. 
# List of proteins of interest can be changed with the true and false HK and RR lists. 
# Can be generalized to just be true and false lists for any proteins, not specifically only HKs and RRs. 

import csv
import collections
import os
import re

# Change working directory path 
os.chdir("/Users/annelisegoldman/TCS_mining/DeMMO1Outputs")

# Input file paths for InterProScan results (this is just the first file in the working directory), 
# true and false HK and RR lists. All files should be in .tsv format.
IPRresults = "/Users/annelisegoldman/TCS_mining/DeMMO1Outputs/orf_DeMMO1_1.fa.tsv"

HKtrue_list = "/Users/annelisegoldman/TCS_mining/DeMMOworkflow/HK1ListTSV.txt"
HKfalse_list = "/Users/annelisegoldman/TCS_mining/DeMMOworkflow/HKFalseListTSV.txt"
RRtrue_list = "/Users/annelisegoldman/TCS_mining/DeMMOworkflow/RR1ListTSV.txt"
RRfalse_list = "/Users/annelisegoldman/TCS_mining/DeMMOworkflow/RRFalseListShortTSV.txt"

def IPR_results(file):
  #Create dictionary from InterProScan results with ORFs as keys and IPR list as values
  with open(file, "rt") as tsvFile:
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
  for filename in os.listdir("/Users/annelisegoldman/TCS_mining/DeMMO1Outputs"):
    if filename.endswith(".tsv"):
      IPRdict = IPR_results(filename)
      HKfilt = IPR_filter(IPRdict, HKpos, HKneg)
      filtdict[(filename)] = [HKfilt]

    print(str(filtdict.keys()))
    filewriter(filtdict, "DeMMO1_HKs.csv")

  # write results for RRs
  filtdict = {}
  # change directory path
  for filename in os.listdir("/Users/annelisegoldman/TCS_mining/DeMMO1Outputs"):
    if filename.endswith(".tsv"):
      IPRdict = IPR_results(filename)
      RRfilt = IPR_filter(IPRdict, RRpos, RRneg)
      filtdict[(filename)] = [RRfilt]

    print(str(filtdict.keys()))
    filewriter(filtdict, "DeMMO1_RRs.csv")
    
  # write summary file with genome ID, #HKs, and #RRs
  masterDictionary = {}
  # change directory path 
  for filename in os.listdir("/Users/annelisegoldman/TCS_mining/DeMMO1Outputs"):
    if filename.endswith(".tsv"):
      IPRdict = IPR_results(filename)
      HKfilt = IPR_filter(IPRdict, HKpos, HKneg)
      RRfilt = IPR_filter(IPRdict, RRpos, RRneg)
      masterDictionary[str(filename)] = [len(HKfilt), len(RRfilt)]
    
    print(str(len(masterDictionary.keys())))
    # change summary output file name
    masterfilewriter(masterDictionary, "DeMMO1_summary.csv")

# Do the complete filtering based on functions defined above
if __name__ == "__main__":
  main()
