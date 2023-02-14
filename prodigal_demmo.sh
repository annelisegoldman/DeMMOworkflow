#!/bin/sh

# This script analyses all .fa files in a directory with prodigal

# Define paths to Prodigal and subdirectory containing nucleic acid fasta files (.fa)
export PRODIGALPATH="/path/to/Prodigal"
export GENOMEPATH="/path/to/input/files.fa"

cd $GENOMEPATH

# Runs Prodigal on each .fa file in the input directory, and adds the prefix "prodigal_" to the output file
for i in *.fa
do
    $PRODIGALPATH'/prodigal' -i $i -a  prodigal_${i} -q

    sed -i s/\*//g prodigal_${i}

done

# Rename completed files with the extension .faa (fasta amino acid)
for f in *.fa
do
	mv -- "$f" "${f%.fa}.faa"
done
