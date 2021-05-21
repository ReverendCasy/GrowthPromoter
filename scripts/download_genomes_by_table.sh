#!/usr/bin/zsh

if [ ! -d "genome_assemblies" ]; then
mkdir genome_assemblies
fi

#name=( $(awk -F'\t' -e  '($3 ~ /(Complete)|(Chromosome)/) && ($5 != "") {print $2}' $1 | \
#      sed -e 's/ (firmicutes)//g' -e 's/ /_/g') )

#level=( $(awk -F'\t' -e '($3 ~ /(Complete)|(Chromosome)/) && ($5 != "") {print $3}' $1 | \
#          sed 's/ /_/g') )

#acc=( $(awk -F'\t' -e '($3 ~ /(Complete)|(Chromosome)/) && ($5 != "") {print $4}' $1) )

#ftp=( $(awk -F'\t' -e '($3 ~ /(Complete)|(Chromosome)/) && ($5 != "") {print $5}' $1) )


declare -a features=('_assembly_report.txt',
                     '_genomic.fna.gz',
                     '_genomic.gff.gz'
                     )

for ftp in $(awk -F'\t' -e '($3 ~ /(Complete)|(Chromosome)/) && ($5 != "") && ($2 ~ /Bacillus/) {print $5}' $1); do
postfix=$(echo $ftp | rev | cut -d'/' -f1 | rev)
name=$(echo $postfix | cut -d'_' -f1,2)
if [ ! -d genome_assemblies/$name ]; then
mkdir genome_assemblies/$name
fi
for feature in ${features[@]}; do
feature=$(echo $feature | sed 's/,//g')
#echo $ftp/$postix$feature
wget -q -P genome_assemblies/$name $ftp/$postfix$feature
done
done
