#!/usr/bin/zsh
PATH=$PATH:~/prank/bin

if [ ! -d $2 ]; then
mkdir $2
fi

if [ ! -d $2/alignments ]; then
mkdir $2/alignments
fi

if [ ! -d $2/models ]; then
mkdir $2/models
fi

#if [ ! -d $2/refs ]; then
#mkdir $2/refs
#fi

if [ ! -d $2/output ]; then
mkdir $2/output
fi

for cluster in $(ls $1); do
prefix=$(echo $cluster | cut -d'.' -f1)
#prank -protein -d=$1/$cluster -o=$2/alignments/$prefix -iterate=10
#hmmbuild --cpu 72 --amino $2/models/$prefix.hmm $2/alignments/$prefix.best.fas
if [ -f $2/models/$prefix.hmm ]; then
for genome in $(ls $3); do
hmmsearch --max --cpu 72  --tblout $2/output/$genome\_$prefix.hmmout $2/models/$prefix.hmm $3/$genome
done
fi
done

