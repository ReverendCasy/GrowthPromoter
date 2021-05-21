#!/usr/bin/zsh

for line in $(cat $1); do
gcas=( $(esearch -db bioproject -query $line | \
         elink -target assembly | \
         esummary | \
         xtract -pattern DocumentSummary \
         -element BioprojectAccn Genbank | \
         grep $line | \
         awk -F'\t' '{ for (i=1;i<=NF;i++) { if ($i ~ "GCA" || $i == v) print $i } }' v="$line") )

echo "${gcas[1]}\t${gcas[2]}" >> $2

done
