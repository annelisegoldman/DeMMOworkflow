import csv
import collections
import os
import re

# Change working directory to 
os.chdir("/Users/annelisegoldman/Documents/TCS Mining Project/DeMMO1 Outputs")

# Input files for InterProScan results, true and false HK and RR lists. All files should be in .tsv format.
IPRresults = "/Users/annelisegoldman/Documents/TCS Mining Project/DeMMO1 Outputs/orf_DeMMO1_1.fa.tsv"

HKtrue_list = "/Users/annelisegoldman/Documents/TCS Mining Project/HK and RR Lists/HK1ListTSV.txt"
HKfalse_list = "/Users/annelisegoldman/Documents/TCS Mining Project/HK and RR Lists/HKFalseListTSV.txt"
RRtrue_list = "/Users/annelisegoldman/Documents/TCS Mining Project/HK and RR Lists/RR1ListTSV.txt"
RRfalse_list = "/Users/annelisegoldman/Documents/TCS Mining Project/HK and RR Lists/RRFalseListShortTSV.txt"

def IPR_results(file):
  #Create dictionary from InterProScan results with ORFs as keys and IPR list as values
  with open(file, "r") as tsvFile:
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
  # Create dictionary (posdict) containing only OFRs with at least one true associated IPR signature 
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

def IPR_filter2(IPRdict, pos_list, neg_list, adddomain_list): # Filters ORFS for IPRs matching true (but not false) IPR signatures AND additional domain IPR signature
  posdict2 = {}
  filtdict2 = {}
  adddomdict = {}
  pos_set2 = set(pos_list)
  neg_set2 = set(neg_list)
  adddom_set = set(adddomain_list)
  # Create dictionary (posdict) containing only OFRs with at least one true associated IPR signature 
  for key, val in IPRdict.items():
    val_set = set(val)
    if len(val_set.intersection(pos_set2)) > 0:
      posdict2[key] = val
  # Create dictionary containing only ORFs with at least one true IPR signature but not one of the false IPR signatures
  for key, val in posdict2.items():
    val_set = set(val)
    if len(val_set.intersection(neg_set2)) == 0:
      filtdict2[key] = val
  # Create dictionary containing only ORFs with at least one true IPR signature but not one of the false IPR signatures AND one of the additional domains 
  for key, val in filtdict2.items():
    val_set = set(val)
    if len(val_set.intersection(adddom_set)) > 0:
      adddomdict[key] = val
  return adddomdict

def masterfilewriter(masterDictionary, fileout): # Writes .csv file containing a summary of all the HKs and RRs filtered from a directory
  cats = masterDictionary.keys()
  with open(fileout, "w") as outfile:
    wr = csv.writer(outfile)
    headers=["Genome","# HKs","# RRs","# HHKs"]
    wr.writerow(headers)
    for cat in cats:
      data = [cat, masterDictionary[cat][0], masterDictionary[cat][1], masterDictionary[cat][2]]
      wr.writerow(data)

def main():
  HKpos = IPR_list(HKtrue_list)
  HKneg = IPR_list(HKfalse_list)
  RRpos = IPR_list(RRtrue_list)
  RRneg = IPR_list(RRfalse_list)

  masterDictionary = {}
  for filename in os.listdir("/Users/annelisegoldman/Documents/TCS Mining Project/DeMMO1 Outputs"):
    if filename.endswith(".tsv"):
      IPRdict = IPR_results(filename)
      HKfilt = IPR_filter(IPRdict, HKpos, HKneg)
      RRfilt = IPR_filter(IPRdict, RRpos, RRneg)
      HHKfilt = IPR_filter2(IPRdict, HKpos, HKneg, RRpos)
      masterDictionary[str(filename)] = [len(HKfilt), len(RRfilt), len(HHKfilt)]
    
    print(str(len(masterDictionary.keys())))
    masterfilewriter(masterDictionary, "DeMMO1_HHKs.csv")

if __name__ == "__main__":
  main()
