# Identifying protein sequences from Interproscan

This project consists of a series of scripts to use [InterProScan](https://github.com/ebi-pf-team/interproscan) to identify two component system (TCS) proteins from prokaryotic genomes and [seqtk](https://github.com/lh3/seqtk) to pull TCS sequences out of whole genomes. We used [Prodigal](https://github.com/hyattpd/Prodigal) to predict putative protein sequences from genomes. 

## Getting Started 

This series of scripts is used as post-processing and assumes that genomes have already been run through InterProScan. The output should be a .tsv file for each input file (genome) with individual sequence names tagged with InterPro (IPR) signatures. You should also have the putative protein sequence .faa files (again, one for each genome) from Prodigal. Have these files ready to be referenced. Finally, make sure that [seqtk](https://github.com/lh3/seqtk) is installed on your computer.

## Dependencies
- [seqtk](https://github.com/lh3/seqtk)

## Analysing .faa files (need to polish this, but think the outline is there)
1. (If needed) Convert DNA sequences to amino acid sequences
If you are starting with nucleic acid sequences, convert to amino acid sequences. This project used [Prodigal](https://github.com/hyattpd/Prodigal "Prodigal") to generate predicted protein sequences from metagenome-assembled genomes. prodigal_demmo.sh analyzes batches of nucleic acid files using Prodigal.

If starting with this step, define the paths to your Prodigal installation and your nucleic acid .fa files. Then run

`bash prodigal_demmo.sh`

2. Count the number of histidine kinases (HKs) and response regulators (RR) in each amino acid FASTA file.

Define filepaths to .tsv outputs from Interproscan, lists of HK/RR true and false positive IPR signatures, and where you want .csv outputs containing the number of HKs/RRs in each genome file to save. Then run:

`python IPR_filter.py`

3. Extract names of HKs (and IPR signatures associated with each HK) from Interproscan .tsv outputs

Define filepaths to .tsv outputs from Intproscan, and run sequence_filter to generate two output files:
- a .csv file containing the name of each HK protein and any other IPR signatures it contains
- a .lst file containing the name of each HK protein

`python sequence_filter.py`

4. Extract HK sequences from .faa files

Define directory paths for inbox containing .faa files from prodigals, directory containing .lst files generated from sequence_filter.py, and run

`python extract_sequences.py`

extract_sequences.py spawns seqtk_run.sh to extract HK seqeunces and renames them to be identifiable by adding the genome ID to the sequence ID (e.g. 11-1 is genome 11, HK 1)

## File descriptions

### count_fastas.py
This script counts the number of proteins in each .faa file from Prodigal

### IPR_filter.py 
Determines the abundance of histidine kinases (HKs) and response regulators (RR) -- the two protein components of a TCS. It reads .tsv IPR files and creates three .csv files: 1) TCS abundances for all genomes, 2) HKs and associated IPR signatures for all genomes, 3) RRs and associated IPR signatures for all genomes.

### prodigal_demmo.sh
This scripts runs all genome .fasta files in a directory through Prodigal, and moves them through an outbox

### rename_fasta.py
I think this script was supposed to rename fasta files to the numbered ID system we ended up using, but got copied/pasted over with another script by accident. I'll double check if I can find a local copy of the original -- luckily it isn't essential to the pipeline, so if we can't find it I don't think it needs to be re-written.

### sequence_filter.py 
Pulls out only HK sequences from the InterProScan .tsv files (can easily modify to also pull out RRs if desired). Creates two files for every input file (genome): 1) .csv file with the names of the HKs and all the associated IPR signatures (sometimes there are other identifying IPR signatures that can be helpful in later analyses) and 2) .lst file with the sequence names of all HK protein sequences in a given genome. 
***This script must be run before extract_sequences.py***

### extract_sequences.py
Uses the .lst HK protein sequence name files from **sequence_filter.py** to pull out full HK protein sequences from the putative protein sequence (Prodigal) .faa files, rename them based on the genome ID, and assemble them into one long list of HK protein sequences. Creates two intermediate files, genomeID_temp.faa and genomeID_renamed.faa, which contain HK sequences with their original names and HK sequences with new names assigned based on genome ID, respectively. Also creates one final file, allHKseq.faa, with the HK protein sequences, labeled by genome ID, from all genomes. 
References several other scripts: **seqtk_run**. 

### HK1ListTSV.txt, HKFalseListTSV.txt, RR1ListTSV.txt, RRFalseListShortTSV.txt - moved to subdirectory while we organize this
These files are referenced by **IPR_filter.py** and **sequence_filter.py**. They contain the IPR signatures for HKs and RRs as well as the false positive IPR signatures for each. 




