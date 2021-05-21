#!/bin/bash

export LANG=C.UTF-8
export LC_ALL=C.UTF-8

if [ ! -d $2 ]; then
mkdir $2
fi

for file in $(ls $1); do
./checkLengths.py $1/$file | cut -f3 | sort | uniq -c > $2/$file
sed -i -e 's/^\s*//g' -e 's/\s/\t/g' $2/$file
done
