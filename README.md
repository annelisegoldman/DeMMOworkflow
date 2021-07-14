# DeMMOworkflow

This project consists of a series of scripts to use [InterProScan](https://github.com/ebi-pf-team/interproscan) to identify two component system (TCS) proteins from prokaryotic genomes and [seqtk](https://github.com/lh3/seqtk) to pull TCS sequences out of whole genomes. We used [Prodigal](https://github.com/hyattpd/Prodigal) to predict putative protein sequences from genomes. 

## Getting Started 

This series of scripts is used as post-processing and assumes that genomes have already been run through InterProScan. The output should be a .tsv file for each input file (genome) with individual sequence names tagged with InterPro (IPR) signatures. You should also have the putative protein sequence .faa files (again, one for each genome) from Prodigal. Have these files ready to be referenced. Finally, make sure that [seqtk](https://github.com/lh3/seqtk) is installed on your computer. 

### IPR_filter.py 
Determines the abundance of histidine kinases (HKs) and response regulators (RR) -- the two protein components of a TCS. It reads .tsv IPR files and creates three .csv files: 1) TCS abundances for all genomes, 2) HKs and associated IPR signatures for all genomes, 3) RRs and associated IPR signatures for all genomes. 

### sequence_filter.py 
Pulls out only HK sequences from the InterProScan .tsv files (can easily modify to also pull out RRs if desired). Creates two files for every input file (genome): 1) .csv file with the names of the HKs and all the associated IPR signatures (sometimes there are other identifying IPR signatures that can be helpful in later analyses) and 2) .lst file with the sequence names of all HK protein sequences in a given genome. 
***This script must be run before extract_seq.py***

### extract_seq.py
Uses the .lst HK protein sequence name files from **sequence_filter.py** to pull out full HK protein sequences from the putative protein sequence (Prodigal) .faa files, rename them based on the genome ID, and assemble them into one long list of HK protein sequences. Creates two intermediate files, genomeID_temp.faa and genomeID_renamed.faa, which contain HK sequences with their original names and HK sequences with new names assigned based on genome ID, respectively. Also creates one final file, allHKseq.faa, with the HK protein sequences, labeled by genome ID, from all genomes. 
References several other scripts: **rename_fasta.py** and **seqtk_run**. 

### HK1ListTSV.txt, HKFalseListTSV.txt, RR1ListTSV.txt, RRFalseListShortTSV.txt 
These files are referenced by **IPR_filter.py** and **sequence_filter.py**. They contain the IPR signatures for HKs and RRs as well as the false positive IPR signatures for each. 

