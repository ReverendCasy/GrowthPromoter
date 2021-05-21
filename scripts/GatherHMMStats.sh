#!/usr/bin/zsh

assemblies=( $(ls $1 | cut -d'.' -f1,2 | sort | uniq) )
clusters=( $(ls $1 | cut -d'_' -f3,4,5 | cut -d'.' -f1 | sort | uniq) )
#echo ${#clusters}

for asmbl in ${assemblies[@]}; do
#echo $asmbl
for clus in ${clusters[@]}; do
#echo $clus
file="$1/$asmbl.faa_$clus.hmmout"
#echo $file
if [[ -f $file ]]; then
res=$(cat $file | \
 sed -e 's/  \+/\t/g' | \
 sed '2s/ /_/g' | \
 sed 's/ /\t/g' | \
 sed '2s/#_//g' | \
 sed '/#/d' | \
 awk '$5 < thresh' thresh=$2 | \
 wc -l)
#echo 'Yeah'
echo "$asmbl\t$clus\t$res"
fi
done
done
