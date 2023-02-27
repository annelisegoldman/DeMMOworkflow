# Mar 8, 2021
# This script counts the number of protein sequences in the Prodigal fasta files

import csv 
import os
import re
import os.path

# set the base directory 
basedir = "/Users/annelisegoldman/TCS_mining/demmo_faa_backup/"
faa_file = os.path.join(basedir, "11.faa")

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

faadict = fasta_counter(faa_file)

finaldict = {}

for file in os.listdir("/Users/annelisegoldman/TCS_mining/demmo_faa_backup/"):
    if file.endswith(".faa"):
        faadict = fasta_counter(file)
        finaldict[(file)] = [faadict]

filewriter(finaldict, os.path.join(basedir, "DeMMO_gene_counts.csv"))



# def fasta_counter(file):
    # counts the number of proteins in a fasta file
    # each protein identified by the ">" at the beginning 
    # essentially counting the number of ">" in each fasta file
    # countdict = {}
    # for key, val in file.items():
        #val_set = set(val)
        #fh = open(os.path.join(basedir, file))
        #n = 0
        #for line in fh: 
            #if line.startswith(">"): 
                #n += 1 
                #fh.close()
        #val = n
        #countdict[key] = val     

#def filewriter(countdict, fileout):
    # creates and writes a .csv file with the genomes and # genes
    #cats = countdict.keys()
    #with open(fileout, "w") as outfile:
       # wr = csv.writer(outfile)
        #headers = ["Genome", "# Genes"]
       # wr.writerow(headers)
       # for cat in cats:
           # data = [cat, countdict[cat][0]]
            ##wr.writerow(data)

#def main():
    # uses the fasta_counter and filewriter functions to 
    # go through the entire directory of fasta files and count 
    # the number of genes in each file 
    # then add the genome name and count to a .csv file

    #countdict = {}
   # for filename in os.listdir(basedir):
       # if filename.endswith(".faa"):
            #countdict[(filename)] = fasta_counter(filename)
        #filewriter(countdict, os.path.join(basedir, "MAG_gene_counts"))

#f __name__ == "__main__":
   # main()


# Original counting function found online: 
# fh = open(os.path.join(basedir, "12.faa"))
# n = 0
# for line in fh:
    # if line.startswith(">"):
       #  n += 1
# fh.close()