# Mar 8, 2021
# This script counts the number of protein sequences in the Prodigal fasta files

import csv 
import os
import re
import os.path

# set the base directory where your amino acid fasta (.faa) files are stored
basedir = "path/to/basedir"

def fasta_counter(filename):
    # counts the number of proteins in a fasta file
    # each protein identified by the ">" at the beginning 
    # essentially counting the number of ">" in each fasta file
    with open(os.path.join(basedir, filename), "rt") as fastaFile:
        gene_num = {}
        for line in fastaFile: 
            num = len([1 for line in open(filename) if line.startswith(">")])
            gene_num[(filename)] = num
    return gene_num

def filewriter(countdict, fileout):
    cats = countdict.keys()
    with open(fileout, "w") as outfile:
        wr = csv.writer(outfile)
        headers = ["Genome", "# genes"]
        wr.writerow(headers)
        for cat in cats:
            data = [cat, countdict[cat][0]]
            wr.writerow(data)

def main():
    finaldict = {}

    for file in os.listdir(basedir):
        if file.endswith(".faa"):
            faadict = fasta_counter(file)
            finaldict[(file)] = [faadict]

    filewriter(finaldict, os.path.join(basedir, "gene_counts.csv"))

if __name__ == "__main__":
  main()