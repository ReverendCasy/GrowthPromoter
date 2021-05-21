#!/usr/bin/zsh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

#if [ ! -d filtered_proteins ]; then
#mkdir filtered_proteins
#fi

#if [ ! -d filtered_proteins/complete ]; then
#mkdir filtered_proteins/complete
#fi

#if [ ! -d filtered_proteins/partial ]; then
#mkdir filtered_proteins/partial
#fi


### Filter sequences explicitly stated to be partial
#for raw_file in $(find protein_templates/*); do
#fpref=$(echo $raw_file | cut -d'/' -f2 | cut -d'.' -f1)
#./filterPartials.py -i $raw_file -o filtered_proteins -p $fpref
#mv filtered_proteins/$fpref\_complete.fasta filtered_proteins/complete/
#mv filtered_proteins/$fpref\_partial.fasta filtered_proteins/partial/
#done


### Among the sequences left, estimate the truly complete ones 
### by aligning them to the partial subject with BLAST

#if [ ! -d blast_res ]; then
#mkdir blast_res
#fi

#if [ ! -d blast_res/db ]; then
#mkdir blast_res/db
#fi

#if [ ! -d blast_res/tables ]; then
#mkdir blast_res/tables
#fi

#if [ ! -d blast_res/preserved_seqs ]; then
#mkdir blast_res/preserved_seqs
#fi

#for partial_file in $(ls filtered_proteins/partial); do
#if [ $(grep -c '>' filtered_proteins/partial/$partial_file) -gt 0 ]; then
#prefix=$(echo $partial_file | cut -d'_' -f1)
#makeblastdb \
# -dbtype prot \
# -in filtered_proteins/partial/$partial_file \
# -title $prefix \
# -out $prefix

#mv $prefix.p* blast_res/db/

#blastp \
# -num_threads 72 \
# -query filtered_proteins/complete/$prefix\_complete.fasta \
# -db blast_res/db/$prefix \
# -qcov_hsp_perc 98 \
# -out blast_res/tables/$prefix.outfmt6 \
# -outfmt "6 qseqid sseqid evalue pident qlen slen length qcovhsp"


#if [ $(wc -l blast_res/tables/$prefix.outfmt6 | cut -d' ' -f1) -gt  0 ]; then
#./filterByBlast.py \
# -s filtered_proteins/complete/$prefix\_complete.fasta \
# -t blast_res/tables/$prefix.outfmt6 \
# -o blast_res/preserved_seqs/$prefix\_filtered.fasta \
# -m abs
#else
#cp filtered_proteins/complete/$prefix\_complete.fasta \
# blast_res/preserved_seqs/$prefix\_filtered.fasta
#fi
#else
#cp filtered_proteins/complete/$prefix\_complete.fasta \
# blast_res/preserved_seqs/$prefix\_filtered.fasta
#fi
#done

### Launch CD-HIT on the remaining complete sequences

if [ ! -d cdhit_res ]; then
mkdir cdhit_res
fi

if [ ! -d cdhit_res/clustering_results ]; then
mkdir cdhit_res/clustering_results
fi

if [ ! -d cdhit_res/clustered_sequences ]; then
mkdir cdhit_res/clustered_sequences
fi

for filt_file in $(ls blast_res/preserved_seqs); do
filt_file=$(echo $filt_file | cut -d'_' -f1)
cd-hit -i blast_res/preserved_seqs/$filt_file\_filtered.fasta -o cdhit_res/clustering_results/$filt_file \
 -M 0 -T 72 -n 4 -c 0.8 -s 0.9
./binCdHit.py -c cdhit_res/clustering_results/$filt_file.clstr -s filtered_proteins/complete/$filt_file\_complete.fasta \
 -o cdhit_res/clustered_sequences
done

### Find a domain layout for all the resulting clusters,
### then merge the clusters with similar layouts

#if [ ! -d interpro_results ]; then
#mkdir interpro_results
#fi

#if [ ! -d interpro_results/tables ]; then
#mkdir interpro_results/tables
#fi

#if [ ! -d interpro_results/merged_clusters ]; then
#mkdir interpro_results/merged_clusters
#fi

#for cluster in $(ls cdhit_res/clustered_sequences); do
#gene_name=$(echo $cluster | cut -d'_' -f1)
#cluster_name=$(echo $cluster | cut -d'.' -f1)

#sudo docker run \
# -it \
# --rm \
# -v `pwd`:/data \
# blaxterlab/interproscan:latest \
# interproscan.sh \
# -i /data/cdhit_res/clustered_sequences/$cluster \
# -o /data/interpro_results/tables/$cluster_name.tsv

#### Incorporate merge_master.py
# <>

### Gather statistics
# <>

### Launch HMMER

#done

### Build models with HMMer



### Launch the resulting models against the genomes
