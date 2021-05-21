#1/usr/bin/zsh

export LANG=C.UTF-8
export LC_ALL=C.UTF-8

if [ ! -d $2 ]; then
mkdir $2
fi

for subdir in $(ls $1); do
find $1/$subdir/* -name '*fna*' -exec cp {} $2 \;
find $1/$subdir/* -name '*gff*' -exec cp {} $2 \;
gunzip $2/*gz

fna=$(ls $2 | grep 'genomic.fna$')
gff=$(ls $2 | grep 'genomic.gff$')

awk -F'\t' '($3=="CDS") {OFS="\t"; print $1,$4-1,$5,$7}' $2/$gff > $2/$subdir.bed
#zcat $fna > $2/$subdir.tmp2
bedtools getfasta -fi $2/$fna -bed $2/$subdir.bed -fo $2/$subdir.fna
rm $2/$gff
rm $2/$fna
rm $2/$fna.fai
./translateFromBED.py -b $2/$subdir.bed -f $2/$subdir.fna -o $2/$subdir.faa
rm $2/$subdir.bed
#rm $2/$subdir.tmp2
rm $2/$subdir.fna
done
