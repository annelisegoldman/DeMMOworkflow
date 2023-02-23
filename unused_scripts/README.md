This directory contains scripts that either weren't used to generate data for the manuscript, or were never debugged. Archiving here until we confirm these aren't needed and can delete.

### calc_IPR_frequency.py
This script counts the number of IPR signatures (i.e. protein domains) associated with the HK sequences at the DeMMO sites. It calculates frequency metrics for how often each IPR signature occurs in the DeMMO site(s).
I don't think we actually used this in the MS, might be able to remove

### seqtk_error_check.py
This script was written to make sure we were pulling out all the HK sequences from the proteome files. (We were. Not sure this is necessary to include)

### count_fastas_oldversion.py
I took a lot of commented code out of this, preserving the older version just in case

### extract_seq.py
A draft of extract_sequences (I think) - it extracts the sequences, but doesn't deal with the renaming part

extract_seq eventually got combined into extract_sequences with additional code to deal with renaming HK sequences to be identifiable

### rename_fasta.py
Exactly the same as extract_sequences. I think it got copied + renamed to match its function

### 102521_phylum_geochem_HKcount.ipynb
Generates figures with correlations between geochemical parameters and HK abundance separated by taxa. I don't think these figures are in the paper or supplement

### 220801_violin_stats.ipynb
Performs statistics calculations on HK distributions in Fig 1. I combined it with "091421_fig1.ipynb" since it was short and uses the same dataset

### SSN_gtdb_phylum_ist.csv
I can't remember what this was used for... maybe color-coding the SSN?