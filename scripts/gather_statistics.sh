#!/usr/bin/zsh

if [ ! -d $2 ]; then
mkdir $2
fi

for prefix in $(ls $1 | cut -d'_' -f1 | sort | uniq); do
    find $1/* \
     -name "$prefix*" \
     -exec grep \
           --with-filename \
           -c \
           '>' \
           {} \; | \
    sed 's/:/_/g' | \
    cut -d'_' \
        -f2,5 | \
    cut -d'/' \
        -f2 | \
    cut -d'_' -f2 > $2/$prefix.txt

done
