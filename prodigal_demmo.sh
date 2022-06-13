#!/bin/sh

export PRODIGALPATH="/home/iancampbell/Prodigal-GoogleImport"
export DEMMOPATH="/home/iancampbell/TCS_mining/DeMMO_genomes/White_Creek"

cd $DEMMOPATH

for i in *.fa
do
    $PRODIGALPATH'/prodigal' -i $i -a  prodigal_${i} -q

    sed -i s/\*//g prodigal_${i}

done

for f in *.fa
do
	mv -- "$f" "${f%.fa}.faa"
done
